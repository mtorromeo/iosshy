# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QDialog, QIcon, QAction, QKeySequence, QListWidgetItem, QItemSelectionModel
from PyQt4.QtCore import Qt, pyqtSignature, QSettings
from tunnel import Tunnel
from tray import Tray
from Ui_tunneldialog import Ui_TunnelDialog

class TunnelDialog(QDialog, Ui_TunnelDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self._explicitQuit = False

		# Tunnels
		self._tunnels = []

		# Setup tray
		self.tray = Tray("IOSSHy", QIcon(":/icons/network-server.png"))
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

		action = QAction("&Quit", self.tray.menu)
		action.setIcon(QIcon(":/icons/application-exit.png"))
		action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
		action.triggered.connect(self.quit)
		self.tray.menu.addAction(action)

		# Load settings
		self.readSettings()

	def closeEvent(self, event):
		if not self._explicitQuit:
			self.hide()
			event.ignore()

	def on_listTunnels_currentItemChanged(self, current, previous):
		self.grpTunnelProperties.setEnabled(current is not None)
		if current is not None:
			tunnel = self._tunnels[self.listTunnels.row(current)]

			self.txtName.setText( tunnel.name )
			self.txtHost.setText( "localhost" if tunnel.host == "" else tunnel.host )
			self.txtLocalPort.setText( "" if tunnel.localPort is None else str(tunnel.localPort) )
			self.txtPort.setText( str(tunnel.port) )
			self.txtUsername.setText( "root" if tunnel.username == "" else tunnel.username )
			self.txtPassword.setText( "" if tunnel.password is None else tunnel.password )
			self.txtCommand.setText( "" if tunnel.command is None else tunnel.command )
			self.chkCloseOnTerm.setChecked( Qt.Checked if tunnel.autoClose else Qt.Unchecked )

			self.txtName.setFocus()
			self.txtName.selectAll()
		else:
			self.txtName.setText("")
			self.txtHost.setText("")
			self.txtLocalPort.setText("")
			self.txtPort.setText("")
			self.txtUsername.setText("")
			self.txtPassword.setText("")
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

	def on_txtUsername_textEdited(self, text):
		self.currentTunnel().username = text

	def on_txtPassword_textEdited(self, text):
		self.currentTunnel().password = text

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
			tunnel.password = cur.password
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

	def quit(self):
		self.writeSettings()
		self._explicitQuit = True
		self.close()