# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.QtGui import QIcon
try:
    from PyKDE4.kdeui import KStatusNotifierItem, KMenu
    kde = True
except ImportError:
    from PyQt4.QtGui import QSystemTrayIcon, QMenu
    kde = False

class Tray(QObject):
    activated = pyqtSignal()

    def __init__(self, parent, title, icon):
        QObject.__init__(self)

        # Setup contextual menu
        if kde:
            self.menu = KMenu(parent)
            self.tray = KStatusNotifierItem(parent)
            self.tray.setStatus(KStatusNotifierItem.Active)
            self.tray.setCategory(KStatusNotifierItem.ApplicationStatus)
            self.tray.setAssociatedWidget(parent)
            self.tray.setStandardActionsEnabled(False)
            self.tray.activateRequested.connect(self._activateRequested)
        else:
            self.menu = QMenu()
            self.tray = QSystemTrayIcon()
            self.tray.activated.connect(self._activated)
        self.setIcon(icon)
        self.setTitle(title)
        if not kde:
            self.tray.show()
        self.tray.setContextMenu(self.menu)

    def setTitle(self, title):
        if kde:
            self.tray.setTitle(title)
            self.tray.setToolTipTitle(title)
        else:
            self.tray.setToolTip(title)
        self.menu.setTitle(title)

    def setIcon(self, icon):
        if kde:
            self.tray.setIconByPixmap(icon)
            self.tray.setToolTipIconByPixmap(icon)
        else:
            self.tray.setIcon(icon)

    def showMessage(self, title, message, icon=None):
        if kde:
            self.tray.showMessage(title, message, "network-server")
        else:
            self.tray.showMessage(title, message, QSystemTrayIcon.Information if icon is None else icon)

    def _activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.activated.emit()

    def _activateRequested(self, active, pos):
        self.activated.emit()

