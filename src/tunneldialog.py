# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog, QSystemTrayIcon, QIcon, QMenu, QAction, QKeySequence
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL
from Ui_tunneldialog import Ui_TunnelDialog

class TunnelDialog(QDialog, Ui_TunnelDialog):
	_explicitQuit = False

	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		
		self.context = QMenu(self)
		action = QAction("&Quit", self.context)
		action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
		self.connect(action, SIGNAL("triggered()"), self.quit)
		self.context.addAction(action)
		
		self.tray = QSystemTrayIcon()
		self.tray.setIcon(QIcon(":/icons/list-add.png"))
		self.connect(self.tray, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.trayClicked)
		self.tray.setContextMenu(self.context)
		self.tray.show()
	
	def closeEvent(self, event):
		if not self._explicitQuit:
			self.hide()
			event.ignore()
	
	def on_listTunnels_currentItemChanged(self, current, previous):
		self.grpTunnelProperties.setEnabled(current is not None)
	
	def on_btnAddTunnel_clicked(self):
		pass
	
	def trayClicked(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.show()
	
	def quit(self):
		self._explicitQuit = True
		self.close()