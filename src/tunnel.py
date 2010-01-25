# -*- coding: utf-8 -*-

import paramiko, select, SocketServer
from threading import Thread

class ForwardServer(SocketServer.ThreadingTCPServer):
	daemon_threads = True
	allow_reuse_address = True

class Handler(SocketServer.BaseRequestHandler):
	def handle(self):
		try:
			chan = self.ssh_transport.open_channel('direct-tcpip', (self.chain_host, self.chain_port), self.request.getpeername())
		except Exception, e:
			#verbose('Incoming request to %s:%d failed: %s' % (self.chain_host, self.chain_port, repr(e)))
			return

		if chan is None:
			#verbose('Incoming request to %s:%d was rejected by the SSH server.' % (self.chain_host, self.chain_port))
			return

		#verbose('Connected! Tunnel open %r -> %r -> %r' % (self.request.getpeername(), chan.getpeername(), (self.chain_host, self.chain_port)))
		while True:
			r, w, x = select.select([self.request, chan], [], [])
			if self.request in r:
				data = self.request.recv(1024)
				if len(data) == 0:
					break
				chan.send(data)
			if chan in r:
				data = chan.recv(1024)
				if len(data) == 0:
					break
				self.request.send(data)
		chan.close()
		self.request.close()
		#verbose('Tunnel closed from %r' % (self.request.getpeername(),))

def forward_tunnel(local_port, remote_host, remote_port, transport):
	# this is a little convoluted, but lets me configure things for the Handler
	# object. (SocketServer doesn't give Handlers any way to access the outer
	# server normally.)
	class SubHander(Handler):
		chain_host = remote_host
		chain_port = remote_port
		ssh_transport = transport
	ForwardServer(('', local_port), SubHander).serve_forever()

class TunnelThread(Thread):
	def __init__(self, ssh_server, local_port, ssh_port=22, remote_host="localhost", remote_port=None, username=None, password=None):
		Thread.__init__(self)
		if remote_port is None:
			remote_port = local_port
		self.local_port = local_port
		self.remote_host = remote_host
		self.remote_port = remote_port

		self.ssh_client = paramiko.SSHClient()
		self.ssh_client.load_system_host_keys()
		self.ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
		self.ssh_client.connect(ssh_server, ssh_port, username=username, password=password, look_for_keys=True)

		transport = self.ssh_client.get_transport()

		class SubHander(Handler):
			chain_host = remote_host
			chain_port = remote_port
			ssh_transport = transport
		self.ffwd_server = ForwardServer(('', self.local_port), SubHander)

	def run(self):
		self.ffwd_server.serve_forever()

	def join(self):
		if self.ffwd_server is not None:
			self.ffwd_server.shutdown()
		self.ssh_client.close()
		del self.ffwd_server
		del self.ssh_client
		Thread.join(self)

from PyQt4.QtGui import QAction, QListWidgetItem, QSystemTrayIcon
from PyQt4.QtCore import Qt

class Tunnel(object):
	def __init__(self, parent):
		self._thread = None
		self._parent = parent
		self._name = "New Tunnel"
		self.host = "localhost"
		self.localPort = None
		self.port = 80
		self.username = "root"
		self.password = None
		self.command = None
		self.autoClose = False
		self._action = QAction(self._name, self._parent.context)
		self._action.setCheckable(True)
		self._action.toggled.connect(self.toggle)
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

	def toggle(self, openTunnel):
		if openTunnel:
			openTunnel = self._thread is None
		if openTunnel:
			self.open_()
		else:
			self.close()

	def open_(self):
		try:
			self._parent.tray.showMessage(self.name, "Opening tunnel")
			self._thread = TunnelThread(username=self.username, password=self.password, ssh_server=self.host, local_port=self.localPort, remote_port=self.port)
		except paramiko.BadHostKeyException as message:
			self.close()
			self._parent.tray.showMessage(self.name, str(message), QSystemTrayIcon.Warning)
		except Exception:
			self.close()

		if self._thread is not None:
			self._thread.start()

	def close(self):
		if self._thread is not None:
			self._parent.tray.showMessage(self.name, "Closing tunnel")
			self._thread.join()
			del self._thread
			self._thread = None
		self._action.setChecked(False)