# -*- coding: utf-8 -*-
#
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

from __future__ import absolute_import


###############################################################################
# METADATA
###############################################################################

__prj__ = "Samurai-IDE"
__author__ = "The Samurai-IDE Team"
__mail__ = "7557867+poikilos@users.noreply.github.com"
__url__ = "https://samurai-ide.org"
__source__ = "https://github.com/poikilos/samurai-ide"
__version__ = "3.0-alpha"
__license__ = "GPL3"

###############################################################################
# DOC
###############################################################################

"""Samurai-IDE is a cross-platform integrated development environment (IDE).
Samurai-IDE runs on Linux/X11, Mac OS X and Windows desktop operating systems,
and allows developers to create applications for several purposes using all the
tools and utilities of Samurai-IDE, making the task of writing software easier
and more enjoyable.
"""

###############################################################################
# SET PYQT API 2
###############################################################################

# API_NAMES = ["QDate", "QDateTime", "QString", "QTime", "QUrl", "QTextStream",
#             "QVariant"]

###############################################################################
# START
###############################################################################


def setup_and_run():
    """Load the Core module and trigger the execution."""
    # import only on run
    # Dont import always this, setup.py will fail
    from samurai_ide import core
    from samurai_ide import nresources  # noqa
    from multiprocessing import freeze_support

    # Used to support multiprocessing on windows packages
    freeze_support()

    # Run Samurai-IDE
    core.run_ninja()
