# -*- coding: utf-8 -*-

import sip, os, sys
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from PyQt4.QtCore import QCoreApplication, QTranslator, QLocale, QSettings
from PyQt4.QtGui import QApplication, QSystemTrayIcon

from tunneldialog import TunnelDialog

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setOrganizationName("MTSoft")
	app.setApplicationName("Tunneller")

	if QSystemTrayIcon.isSystemTrayAvailable():
		translator = QTranslator()
		qmFile = "tunneller_%s.qm" % QLocale.system().name()
		if os.path.isfile(qmFile):
			translator.load(qmFile)
		QApplication.installTranslator(translator)

		dialog = TunnelDialog()
		sys.exit(app.exec_())
	else:
		print "System tray not available. Exiting."
		sys.exit(1)