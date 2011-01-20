# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtGui import QIcon, QDialog, QAction, QKeySequence, QListWidgetItem, QItemSelectionModel
from PyQt4.QtCore import Qt, pyqtSignature, QSettings
from tunnel import Tunnel
from tray import Tray
from Ui_tunneldialog import Ui_TunnelDialog

try:
    from PyKDE4.kdeui import KAboutApplicationDialog, KMainWindow
    import application
    kde = True
    class WindowBaseClass(QDialog, KMainWindow): pass
except ImportError:
    kde = False
    class WindowBaseClass(QDialog): pass

class TunnelDialog(WindowBaseClass, Ui_TunnelDialog):
    def __init__(self):
        WindowBaseClass.__init__(self)
        self.setupUi(self)
        self._explicitQuit = False

        # Tunnels
        self._tunnels = []

        # Setup tray
        self.tray = Tray(self, "IOSSHy", QIcon(":/icons/network-server.png"))
        self.tray.activated.connect(self.activated)

        action = QAction("&Configure", self.tray.menu)
        action.setIcon(QIcon(":/icons/configure.png"))
        action.triggered.connect(self.show)
        self.tray.menu.addAction(action)
        self.tray.menu.setDefaultAction(action)

        self.tray.menu.addSeparator()
        self.actionNoTun = QAction("No tunnels configured", self.tray.menu)
        self.actionNoTun.setEnabled(False)
        self.tray.menu.addAction(self.actionNoTun)
        self.actionLastSep = self.tray.menu.addSeparator()

        if kde:
            action = QAction("&About", self.tray.menu)
            action.triggered.connect(self.about)
            self.tray.menu.addAction(action)

        action = QAction("&Quit", self.tray.menu)
        action.setIcon(QIcon(":/icons/application-exit.png"))
        action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
        action.triggered.connect(self.quit)
        self.tray.menu.addAction(action)

        # Load settings
        self.readSettings()
        self.hide()

    def show(self):
        self.visible = True
        WindowBaseClass.show(self)

    def hide(self):
        self.visible = False
        self.writeSettings()
        WindowBaseClass.hide(self)

    def closeEvent(self, event):
        if not self._explicitQuit:
            self.hide()
            event.ignore()

    def on_listTunnels_currentItemChanged(self, current, previous):
        self.grpTunnelProperties.setEnabled(current is not None)
        self.grpSshProperties.setEnabled(current is not None)
        if current is not None:
            tunnel = self._tunnels[self.listTunnels.row(current)]

            self.txtName.setText( tunnel.name )
            self.txtHost.setText( "localhost" if tunnel.host == "" else tunnel.host )
            self.txtLocalPort.setText( "0" if tunnel.localPort is None else str(tunnel.localPort) )
            self.txtPort.setText( str(tunnel.port) )
            self.txtSshPort.setText( str(tunnel.sshPort) )
            self.txtUsername.setText( "root" if tunnel.username == "" else tunnel.username )
            self.txtCommand.setText( "" if tunnel.command is None else tunnel.command )
            self.chkCloseOnTerm.setChecked( Qt.Checked if tunnel.autoClose else Qt.Unchecked )

            self.txtName.setFocus()
            self.txtName.selectAll()
        else:
            self.txtName.setText("")
            self.txtHost.setText("localhost")
            self.txtLocalPort.setText("0")
            self.txtPort.setText("")
            self.txtSshPort.setText("22")
            self.txtUsername.setText("root")
            self.txtCommand.setText("")
            self.chkCloseOnTerm.setChecked(Qt.Unchecked)

    def currentTunnel(self):
        try:
            ti = self.listTunnels.currentRow()
            return None if ti < 0 else self._tunnels[ti]
        except IndexError:
            return None

    def on_txtName_textEdited(self, text):
        self.currentTunnel().name = text

    def on_txtHost_textEdited(self, text):
        self.currentTunnel().host = text

    def on_txtLocalPort_textEdited(self, text):
        self.currentTunnel().localPort = text

    def on_txtPort_textEdited(self, text):
        self.currentTunnel().port = text

    def on_txtSshPort_textEdited(self, text):
        self.currentTunnel().sshPort = text

    def on_txtUsername_textEdited(self, text):
        self.currentTunnel().username = text

    def on_txtCommand_textEdited(self, text):
        self.currentTunnel().command = text

    def on_chkCloseOnTerm_stateChanged(self, state):
        if self.currentTunnel() is not None:
            self.currentTunnel().autoClose = state == Qt.Checked

    @pyqtSignature("")
    def on_btnAddTunnel_clicked(self):
        tunnel = Tunnel(self)
        self._tunnels.append(tunnel)
        self.listTunnels.setCurrentItem(tunnel.item)
        self.tray.menu.insertAction(self.actionLastSep, tunnel.action)
        self.tray.menu.removeAction(self.actionNoTun)

    @pyqtSignature("")
    def on_btnDuplicateTunnel_clicked(self):
        cur = self.currentTunnel()
        if cur is not None:
            tunnel = Tunnel(self)
            tunnel.name = cur.name+" (copy)"
            tunnel.host = cur.host
            tunnel.localPort = cur.localPort
            tunnel.port = cur.port
            tunnel.username = cur.username
            tunnel.command = cur.command
            tunnel.autoClose = cur.autoClose
            self._tunnels.append(tunnel)
            self.listTunnels.setCurrentItem(tunnel.item)
            self.tray.menu.insertAction(self.actionLastSep, tunnel.action)

    @pyqtSignature("")
    def on_btnRemoveTunnel_clicked(self):
        tunnel = self.currentTunnel()
        if tunnel is not None:
            ti = self.listTunnels.currentRow()
            del self._tunnels[ti]
            self.listTunnels.setCurrentRow(0 if ti != 0 else 1)
            self.listTunnels.takeItem(ti)
            self.listTunnels.setCurrentItem(None, QItemSelectionModel.Clear)
            self.tray.menu.removeAction(tunnel.action)
            del tunnel

            if len(self._tunnels) == 0:
                self.tray.menu.insertAction(self.actionLastSep, self.actionNoTun)

    def activated(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def readSettings(self):
        if os.name == 'nt':
            settings = QSettings()
        else:
            settings = QSettings(os.path.expanduser("~/.iosshy.ini"), QSettings.IniFormat)
        for name in settings.childGroups():
            tunnel = Tunnel(self)
            tunnel.name = name
            tunnel.readSettings(settings)
            self._tunnels.append(tunnel)
            self.tray.menu.insertAction(self.actionLastSep, tunnel.action)
            self.tray.menu.removeAction(self.actionNoTun)

    def writeSettings(self):
        if os.name == 'nt':
            settings = QSettings()
        else:
            settings = QSettings(os.path.expanduser("~/.iosshy.ini"), QSettings.IniFormat)
        settings.clear()
        for tunnel in self._tunnels:
            tunnel.writeSettings(settings)

    def about(self):
        KAboutApplicationDialog(application.aboutData, self).exec_()
        if self.isHidden():
            self.show()
            self.hide()

    def quit(self):
        self.writeSettings()
        self._explicitQuit = True
        self.close()
