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

import os
import sys

from PyQt4.QtCore import QObject

from samurai_ide.tools.logger import NinjaLogger


class Plugin(QObject):
    '''
    Base class for ALL Plugin
    All plugins should inherit from this class
    '''

    def __init__(self, locator, metadata=None):
        QObject.__init__(self)
        self.locator = locator
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata
        klass = self.__class__
        plugin_name = "%s.%s" % (klass.__module__, klass.__name__)
        self.logger = NinjaLogger('samurai_ide.plugins.%s' % plugin_name)
        # set the path!
        try:
            self_module = self.__module__
            path = os.path.abspath(sys.modules[self_module].__file__)
            self._path = os.path.dirname(path)
        except BaseException:
            self._path = ''

    def initialize(self):
        """The initialization of the Plugin should be here."""
        self.logger.info("Initializing Plugin...")

    def finish(self):
        pass

    def get_preferences_widget(self):
        pass

    @property
    def path(self):
        return self._path
