# -*- coding: utf-8 -*-

import sip, os, sys
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

import warnings
warnings.filterwarnings("ignore", ".*sha module is deprecated.*", DeprecationWarning)
warnings.filterwarnings("ignore", ".*md5 module is deprecated.*", DeprecationWarning)

from PyQt4.QtCore import QCoreApplication, QTranslator, QLocale, QSettings
from PyQt4.QtGui import QApplication, QSystemTrayIcon

from tunneldialog import TunnelDialog

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setOrganizationName("MTSoft")
	app.setApplicationName("IOSSHy")

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