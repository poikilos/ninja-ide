# This file is part of Samurai-IDE (https://samurai-ide.org).
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
from PyQt5.QtCore import QObject


# FIXME: icon property (we can use FontAwesome in text property)


class Tab(QObject):

    def __init__(self, text: str, bar=None):
        super().__init__(bar)
        self._text = text
        self._tooltip: str = None

    @property
    def text(self) -> str:
        return self._text

    @property
    def tooltip(self) -> str:
        return self._tooltip
