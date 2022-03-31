# -*- coding: utf-8 -*-
#
# This file is part of Samurai-IDE (http://ninja-ide.org).
#
# Samurai-IDE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Samurai-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Samurai-IDE; If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import sys

try:
    if sys.platform == 'win32':
        from samurai_ide.core.file_handling.filesystem_notifications import windows
        source = windows
    elif sys.platform == 'darwin':
        from samurai_ide.core.file_handling.filesystem_notifications import darwin
        source = darwin
    elif sys.platform.startswith("linux"):
        from samurai_ide.core.file_handling.filesystem_notifications import linux
        source = linux
    else:
        # Aything we do not have a clue how to handle
        from samurai_ide.core.file_handling.filesystem_notifications import openbsd
        source = openbsd
except BaseException:
    from samurai_ide.core.file_handling.filesystem_notifications import openbsd
    source = openbsd


NinjaFileSystemWatcher = source.NinjaFileSystemWatcher()
