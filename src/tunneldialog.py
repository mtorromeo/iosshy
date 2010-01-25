# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog, QSystemTrayIcon, QIcon, QMenu, QAction, QKeySequence, QListWidgetItem
from PyQt4.QtCore import Qt, pyqtSignature
from Ui_tunneldialog import Ui_TunnelDialog

class TunnelDialog(QDialog, Ui_TunnelDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self._explicitQuit = False

		# Tunnels
		self._tunnels = []

		# Setup contextual menu
		self.context = QMenu(self)

		action = QAction("&Configure", self.context)
		action.setIcon(QIcon(":/icons/configure.png"))
		action.triggered.connect(self.show)
		self.context.addAction(action)

		action = QAction("&Quit", self.context)
		action.setIcon(QIcon(":/icons/application-exit.png"))
		action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
		action.triggered.connect(self.quit)
		self.context.addAction(action)

		# Setup tray
		self.tray = QSystemTrayIcon()
		self.tray.setIcon(QIcon(":/icons/network-server.png"))
		self.tray.activated.connect(self.trayClicked)
		self.tray.setContextMenu(self.context)
		self.tray.show()

	def closeEvent(self, event):
		if not self._explicitQuit:
			self.hide()
			event.ignore()

	def on_listTunnels_currentItemChanged(self, current, previous):
		self.grpTunnelProperties.setEnabled(current is not None)
		tunnel = self._tunnels[self.listTunnels.row(current)]

		self.txtName.setText( tunnel["name"] )
		self.txtHost.setText( tunnel["host"] )
		self.txtLocalPort.setText( "" if tunnel["localPort"] is None else str(tunnel["localPort"]) )
		self.txtPort.setText( str(tunnel["port"]) )
		self.txtPassword.setText( "" if tunnel["password"] is None else tunnel["password"] )
		self.txtCommand.setText( "" if tunnel["command"] is None else tunnel["command"] )
		self.chkCloseOnTerm.setChecked( Qt.Checked if tunnel["autoClose"] else Qt.Unchecked )

		self.txtName.setFocus()
		self.txtName.selectAll()

	def setCurrentTunnelProperty(self, name, value):
		ti = self.listTunnels.currentRow()
		self._tunnels[ti][name] = value

	def on_txtName_textEdited(self, text):
		self.setCurrentTunnelProperty("name", text)
		self.listTunnels.currentItem().setText(text)

	def on_txtHost_textEdited(self, text):
		self.setCurrentTunnelProperty("host", text)

	def on_txtLocalPort_textEdited(self, text):
		port = int(text)
		if 0 < port < 65536:
			self.setCurrentTunnelProperty("localPort", port)

	def on_txtPort_textEdited(self, text):
		port = int(text)
		if 0 < port < 65536:
			self.setCurrentTunnelProperty("port", port)

	def on_txtPassword_textEdited(self, text):
		self.setCurrentTunnelProperty("password", text)

	def on_txtCommand_textEdited(self, text):
		self.setCurrentTunnelProperty("command", text)

	def on_chkCloseOnTerm_stateChanged(self, state):
		self.setCurrentTunnelProperty("autoClose", state == Qt.Checked)

	def makeNewTunnel(self):
		return dict(
			name = "New Tunnel",
			host = "localhost",
			localPort = None,
			port = 80,
			password = None,
			command = None,
			autoClose = False
		)

	@pyqtSignature("")
	def on_btnAddTunnel_clicked(self):
		tunnel = self.makeNewTunnel()
		self._tunnels.append(tunnel)
		item = QListWidgetItem(tunnel["name"], self.listTunnels)
		self.listTunnels.setCurrentItem(item)

	def trayClicked(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.show()

	def quit(self):
		self._explicitQuit = True
		self.close()