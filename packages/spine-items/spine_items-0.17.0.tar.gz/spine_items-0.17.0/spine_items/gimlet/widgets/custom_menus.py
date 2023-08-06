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
Classes for custom context menus and pop-up menus for Gimlets

:author: P. Savolainen (VTT)
:date:   15.4.2020
"""

from spinetoolbox.widgets.custom_menus import CustomContextMenu


class GimletPropertiesContextMenu(CustomContextMenu):
    """Context menu class for a Gimlet project item properties."""

    def __init__(self, parent, position, index):
        """

        Args:
            parent (QWidget): Parent for menu widget (ToolboxUI)
            position (QPoint): Position on screen
            index (QModelIndex): Index of item that requested the context-menu
        """
        super().__init__(parent, position)
        if not index.isValid():
            # If no item at index
            return
        self.add_action("Open Gimlet")
