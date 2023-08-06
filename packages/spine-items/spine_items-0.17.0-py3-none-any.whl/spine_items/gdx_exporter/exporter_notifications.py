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
Contains :class:`ExporterNotifications`.

:author: A. Soininen (VTT)
:date:   11.1.2022
"""


class ExporterNotifications:
    """
    Holds flags for different exporter error conditions.

    Attributes:
        duplicate_output_file_name (bool): True if there are duplicate output file names
        missing_output_file_name (bool): True if the output file name is missing
        missing_specification (bool): True if export specification is missing
    """

    def __init__(self):
        self.duplicate_output_file_name = False
        self.missing_output_file_name = False
        self.missing_specification = False
