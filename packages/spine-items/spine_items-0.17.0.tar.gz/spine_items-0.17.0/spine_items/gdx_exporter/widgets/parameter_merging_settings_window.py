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
Parameter merging settings window.

:author: A. Soininen (VTT)
:date:   19.2.2020
"""

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import QMessageBox, QWidget
from spinedb_api import DatabaseMapping
from .merging_error_flag import MergingErrorFlag
from .parameter_merging_settings import ParameterMergingSettings


class ParameterMergingSettingsWindow(QWidget):
    """A window which shows a list of ParameterMergingSettings widgets, one for each merged parameter."""

    settings_approved = Signal()
    """Emitted when the settings have been approved."""
    settings_rejected = Signal()
    """Emitted when the settings have been rejected."""

    def __init__(self, merging_settings, set_settings, database_path, parent):
        """
        Args:
            merging_settings (dict): a map from merged parameter name to a list of merging settings
            set_settings (SetSettings): set settings
            database_path (str): database URL
            parent (QWidget): a parent widget
        """
        from ..ui.parameter_merging_settings_window import Ui_Form  # pylint: disable=import-outside-toplevel

        super().__init__(parent, f=Qt.Window)
        self._merging_settings = merging_settings
        self._set_settings = set_settings
        self._entity_class_infos = None
        self._database_url = database_path
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self.setWindowTitle(f"Gdx Parameter Merging Settings")
        self._setting_widgets = list()
        for parameter_name, setting_list in merging_settings.items():
            for setting in setting_list:
                self._add_setting(parameter_name, setting)
        self._ui.button_box.accepted.connect(self._collect_and_hide)
        self._ui.button_box.rejected.connect(self._reject_and_close)
        self._ui.add_button.setEnabled(bool(database_path))
        self._ui.add_button.clicked.connect(self._add_empty_setting)

    @property
    def merging_settings(self):
        """a dict that maps merged parameter names to their merging settings"""
        return self._merging_settings

    def update(self):
        """Updates the settings according to changes in the database."""
        db_map = DatabaseMapping(self._database_url)
        try:
            self._entity_class_infos = _gather_entity_class_infos(db_map)
        finally:
            db_map.connection.close()
        for settings_widget in self._setting_widgets:
            settings_widget.update(self._entity_class_infos)

    def _add_setting(self, parameter_name=None, merging_setting=None):
        """Inserts a new settings widget to the widget list."""
        if self._entity_class_infos is None:
            if self._database_url:
                db_map = DatabaseMapping(self._database_url)
                try:
                    self._entity_class_infos = _gather_entity_class_infos(db_map)
                finally:
                    db_map.connection.close()
            else:
                self._entity_class_infos = _rebuild_entity_class_infos(self._merging_settings)
        settings_widget = ParameterMergingSettings(
            self._entity_class_infos, self._set_settings, self, parameter_name, merging_setting
        )
        settings_widget.removal_requested.connect(self._remove_setting)
        self._ui.settings_area_layout.insertWidget(0, settings_widget)
        self._setting_widgets.append(settings_widget)

    def _ok_to_accept(self):
        """Returns True if it is OK to accept the settings, otherwise shows a warning dialog and returns False."""
        for settings_widget in self._setting_widgets:
            flags = settings_widget.error_flags
            if flags & MergingErrorFlag.PARAMETER_NAME_MISSING:
                self._ui.setting_area.ensureWidgetVisible(settings_widget)
                message = "Parameter name is missing."
                QMessageBox.warning(self, "Parameter Name Missing", message)
                return False
            if flags & MergingErrorFlag.DOMAIN_NAME_MISSING:
                self._ui.setting_area.ensureWidgetVisible(settings_widget)
                message = "Domain name is missing."
                QMessageBox.warning(self, "Domain Name Missing", message)
                return False
            if flags & MergingErrorFlag.NO_PARAMETER_SELECTED:
                self._ui.setting_area.ensureWidgetVisible(settings_widget)
                message = "No domain selected for parameter merging."
                QMessageBox.warning(self, "Domain Selection Missing", message)
                return False
            if flags & MergingErrorFlag.DOMAIN_NAME_CLASH:
                self._ui.setting_area.ensureWidgetVisible(settings_widget)
                message = "A set with the same name already exists."
                QMessageBox.warning(self, "Invalid Domain Name", message)
                return False
        return True

    @Slot(bool)
    def _add_empty_setting(self, _):
        """Adds an empty settings widget to the widget list."""
        self._add_setting()

    @Slot(object)
    def _remove_setting(self, settings_widget):
        """Removes a setting widget from the widget list."""
        self._setting_widgets.remove(settings_widget)
        self._ui.settings_area_layout.removeWidget(settings_widget)
        settings_widget.deleteLater()

    @Slot()
    def _collect_and_hide(self):
        """Collects settings from individual ParameterMergingSettings widgets and hides the window."""
        if not self._ok_to_accept():
            return
        settings = dict()
        for widget in self._setting_widgets:
            setting_list = settings.setdefault(widget.parameter_name, list())
            setting_list.append(widget.merging_setting())
        self._merging_settings = settings
        self.settings_approved.emit()
        self.hide()

    @Slot()
    def _reject_and_close(self):
        """Emits settings_rejected and closes the window."""
        self.settings_rejected.emit()
        self.close()


class EntityClassInfo:
    """
    Contains information of an object_class or a relationship_class for use in the parameter merging widget.

    Attributes:
        name (str): entity class' name
        domain_names (tuple of str): object classes that index the entities in this class; for object classes this list
            contains the entity's name only, for relationship classes the list contains the relationship's object
            classes
        parameter_names (list of str): entity's defined parameters
    """

    def __init__(self, name, domain_names, parameter_names):
        """
        Args:
            name (str): entity class' name
            domain_names (tuple of str): object classes that index the entities in this class; for object classes it
                contains the entity's name only, for relationship classes it contains the relationship's object
                classes
            parameter_names (list of str): entity's defined parameters
        """
        self.name = name
        self.domain_names = domain_names
        self.parameter_names = parameter_names


def _gather_entity_class_infos(db_map):
    """
    Collects entity_class infos from database.

    Args:
        db_map (spinedb_api.DatabaseMapping): a database map
    Returns:
        list: a list of EntityClassInfo objects
    """
    infos = list()
    for object_class in db_map.query(db_map.object_class_sq):
        class_id = object_class.id
        parameter_definitions = db_map.query(db_map.parameter_definition_sq).filter_by(object_class_id=class_id)
        parameter_names = [definition.name for definition in parameter_definitions]
        infos.append(EntityClassInfo(object_class.name, (object_class.name,), parameter_names))
    for relationship_class in db_map.query(db_map.wide_relationship_class_sq):
        class_id = relationship_class.id
        parameter_definitions = db_map.query(db_map.parameter_definition_sq).filter_by(relationship_class_id=class_id)
        parameter_names = [definition.name for definition in parameter_definitions]
        domain_names = tuple(relationship_class.object_class_name_list.split(","))
        infos.append(EntityClassInfo(relationship_class.name, domain_names, parameter_names))
    return infos


def _rebuild_entity_class_infos(merging_settings):
    """
    Rebuilds entity class infos from given parameter merging settings.

    Args:
        merging_settings (dict): merging settings

    Returns:
        list of EntityClassInfo: entity class infos
    """
    infos = list()
    for settings_list in merging_settings.values():
        for merging_setting in settings_list:
            infos.append(
                EntityClassInfo(
                    merging_setting.previous_set, merging_setting.previous_domain_names, merging_setting.parameter_names
                )
            )
    return infos
