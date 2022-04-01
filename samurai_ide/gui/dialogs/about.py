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

import webbrowser

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QPushButton,
    QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import (
    Qt,
    QSize
)

import samurai_ide
from samurai_ide import translations


class AboutProgram(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowTitle(self.tr("About Samurai-IDE"))
        self.setMaximumSize(QSize(0, 0))

        vbox = QVBoxLayout(self)

        # Create an icon for the Dialog
        pixmap = QPixmap(":img/icon")
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(pixmap)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lblIcon)

        lblTitle = QLabel(
            '<h1>Samurai-IDE</h1>\n<i>Samurai-IDE is the Same But More Active Involvement IDE<i>')
        lblTitle.setTextFormat(Qt.RichText)
        lblTitle.setAlignment(Qt.AlignLeft)
        hbox.addWidget(lblTitle)
        vbox.addLayout(hbox)
        # Add description
        vbox.addWidget(QLabel(
            self.tr("""Samurai-IDE (from: "Same But More Active Involvement IDE"), is a
cross-platform integrated development environment specifically
designed to build Python Applications.

Samurai-IDE provides the tools necessary to simplify the
Python software development process and handles all kinds of
situations thanks to its rich extensibility.""")))
        vbox.addWidget(QLabel(self.tr("Version: %s") % samurai_ide.__version__))
        link_ninja = QLabel(
            self.tr('Website: <a href="%s"><span style=" '
                    'text-decoration: underline; color:#ff9e21;">'
                    '%s</span></a>') %
            (samurai_ide.__url__, samurai_ide.__url__))
        vbox.addWidget(link_ninja)
        link_source = QLabel(
            self.tr('Source Code: <a href="%s"><span style=" '
                    'text-decoration: underline; color:#ff9e21;">%s</span></a>') %
            (samurai_ide.__source__, samurai_ide.__source__))
        vbox.addWidget(link_source)

        hbox2 = QHBoxLayout()
        hbox2.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        btn_close = QPushButton(translations.TR_CLOSE)
        hbox2.addWidget(btn_close)
        vbox.addLayout(hbox2)

        # FIXME: setOpenExternalLinks on labels
        link_ninja.linkActivated['QString'].connect(self.link_activated)
        link_source.linkActivated['QString'].connect(self.link_activated)
        btn_close.clicked.connect(self.close)

    def link_activated(self, link):
        webbrowser.open(str(link))
