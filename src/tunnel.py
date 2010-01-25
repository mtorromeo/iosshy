# -*- coding: utf-8 -*-

from PyQt4.QtGui import QAction
from PyQt4.QtCore import Qt

class Tunnel(object):
	def __init__(self, parent):
		self._parent = parent
		self._name = "New Tunnel"
		self.host = "localhost"
		self.localPort = None
		self.port = 80
		self.password = None
		self.command = None
		self.autoClose = False
		self._action = QAction(self._name, self._parent.context)
		self._item = QListWidgetItem(self._name, self._parent.listTunnels)

	def getAction(self):
		return self._action

	def getItem(self):
		return self._item

	def getName(self):
		return self._name

	def setName(self, name):
		self._name = name
		self._action.setText(name)
		self._item.setText(name)

	name = property(getName, setName)
	action = property(getAction)
	item = property(getItem)