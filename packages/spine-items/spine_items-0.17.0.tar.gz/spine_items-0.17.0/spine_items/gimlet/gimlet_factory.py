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
The GimletFactory class.

:author: P. Savolainen (VTT)
:date:   22.4.2020
"""

from PySide2.QtGui import QColor
from spinetoolbox.project_item.project_item_factory import ProjectItemFactory
from .gimlet import Gimlet
from .gimlet_icon import GimletIcon
from .widgets.gimlet_properties_widget import GimletPropertiesWidget
from .widgets.add_gimlet_widget import AddGimletWidget


class GimletFactory(ProjectItemFactory):
    @staticmethod
    def item_class():
        return Gimlet

    @staticmethod
    def icon():
        return ":/icons/item_icons/screwdriver.svg"

    @staticmethod
    def icon_color():
        return QColor("orange")

    @staticmethod
    def make_add_item_widget(toolbox, x, y, specification):
        return AddGimletWidget(toolbox, x, y, specification)

    @staticmethod
    def make_icon(toolbox):
        return GimletIcon(toolbox, GimletFactory.icon(), GimletFactory.icon_color())

    @staticmethod
    def make_item(name, item_dict, toolbox, project):
        return Gimlet.from_dict(name, item_dict, toolbox, project)

    @staticmethod
    def make_properties_widget(toolbox):
        return GimletPropertiesWidget(toolbox)

    @staticmethod
    def make_specification_menu(parent, index):
        raise NotImplementedError()

    @staticmethod
    def make_specification_editor(toolbox, specification=None, item=None, **kwargs):
        """See base class."""
        raise NotImplementedError()
