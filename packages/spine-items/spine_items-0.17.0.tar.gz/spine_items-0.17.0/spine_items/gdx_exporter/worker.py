######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
A worker based machinery to construct the settings data structures needed for gdx export outside the UI loop.

:author: A. Soininen (VTT)
:date:   19.12.2019
"""

from copy import deepcopy
from PySide2.QtCore import QObject, QThread, Signal, Slot
from spinedb_api import DatabaseMapping, SpineDBAPIError
from spinedb_api.spine_io.exporters import gdx


class Worker(QObject):
    """
    A worker to construct export settings for a database.

    Attributes:
        thread (QThread): the thread the worker executes in
        database_url (str): database URL
    """

    database_unavailable = Signal()
    """Emitted when opening the database fails."""
    errored = Signal(object)
    """Emitted when an error occurs."""
    finished = Signal(object)
    """Emitted when the worker has finished."""

    def __init__(self, database_url, none_fallback, logger):
        """
        Args:
            database_url (str): database's URL
            none_fallback (NoneFallback): how to handle None parameter values
            logger (LoggerInterface): a logger
        """
        super().__init__()
        self.thread = QThread()
        self.moveToThread(self.thread)
        self._none_fallback = none_fallback
        self.database_url = str(database_url)
        self._previous_settings = None
        self._previous_indexing_settings = None
        self._previous_merging_settings = None
        self._logger = logger
        self.thread.started.connect(self._fetch_settings)

    @Slot()
    def _fetch_settings(self):
        """Constructs settings and parameter index settings."""
        result = _Result(*self._read_settings())
        if result.set_settings is None:
            return
        if self._previous_settings is not None:
            updated_settings = deepcopy(self._previous_settings)
            try:
                updated_settings.update(result.set_settings)
            except gdx.GdxExportException as error:
                self.errored.emit(str(error))
                return
            updated_indexing_settings = self._update_indexing_settings(result.indexing_settings)
            if updated_indexing_settings is None:
                return
            updated_merging_settings = self._update_merging_settings(updated_settings)
            if updated_merging_settings is None:
                return
            result.set_settings = updated_settings
            result.indexing_settings = updated_indexing_settings
            result.merging_settings = updated_merging_settings
        self.finished.emit(result)
        self.thread.quit()

    def set_previous_settings(self, previous_settings, previous_indexing_settings, previous_merging_settings):
        """
        Makes worker update existing settings instead of just making new ones.

        Args:
            previous_settings (gdx.SetSettings): existing set settings
            previous_indexing_settings (dict): existing indexing settings
            previous_merging_settings (dict): existing merging settings
        """
        self._previous_settings = previous_settings
        self._previous_indexing_settings = previous_indexing_settings
        self._previous_merging_settings = previous_merging_settings

    def _read_settings(self):
        """Reads fresh gdx settings from the database."""
        try:
            database_map = DatabaseMapping(self.database_url)
        except SpineDBAPIError:
            self.database_unavailable.emit()
            return None, None
        try:
            settings = gdx.make_set_settings(database_map)
            indexing_settings = gdx.make_indexing_settings(database_map, self._none_fallback, self._logger)
        except gdx.GdxExportException as error:
            self.errored.emit(error)
            return None, None
        finally:
            database_map.connection.close()
        return settings, indexing_settings

    def _update_indexing_settings(self, new_indexing_settings):
        """Updates the parameter indexing settings according to changes in the database."""
        updated_indexing_settings = gdx.update_indexing_settings(
            self._previous_indexing_settings, new_indexing_settings
        )
        return updated_indexing_settings

    def _update_merging_settings(self, updated_settings):
        """Updates the parameter merging settings according to changes in the database"""
        try:
            database_map = DatabaseMapping(self.database_url)
        except SpineDBAPIError as error:
            self.errored.emit(error)
            return None
        try:
            updated_merging_settings = gdx.update_merging_settings(
                self._previous_merging_settings, updated_settings, database_map
            )
        except gdx.GdxExportException as error:
            self.errored.emit(error)
            return None
        finally:
            database_map.connection.close()
        return updated_merging_settings


class _Result:
    """
    Contains fetched export settings.

    Attributes:
        set_settings (gdx.SetSettings): gdx export settings
        indexing_settings (dict): parameter indexing settings
        merging_settings (dict): parameter merging settings
    """

    def __init__(self, set_settings, indexing_settings):
        """
        Args:
            set_settings (gdx.SetSettings): gdx export settings
            indexing_settings (dict): parameter indexing settings
        """
        self.set_settings = set_settings
        self.indexing_settings = indexing_settings
        self.merging_settings = dict()
