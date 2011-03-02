# -*- coding: utf-8 -*-

import sip, os, sys
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

import warnings
warnings.filterwarnings("ignore", ".*sha module is deprecated.*", DeprecationWarning)
warnings.filterwarnings("ignore", ".*md5 module is deprecated.*", DeprecationWarning)
warnings.filterwarnings("ignore", ".*This application uses RandomPool.*", DeprecationWarning)

app = None
aboutData = None

name = "IOSSHy"
description = "Desktop tool to quickly setup SSH tunnels and automatically execute commands that make use of them"
version = "1.6"
url = "http://github.com/mtorromeo/iosshy"

def main():
    global app, aboutData

    import setproctitle
    setproctitle.setproctitle("iosshy")

    from PyQt4.QtCore import QCoreApplication, QTranslator, QLocale, QSettings
    from PyQt4.QtGui import QApplication, QSystemTrayIcon, QImage

    from tunneldialog import TunnelDialog

    try:
        from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
        from PyKDE4.kdeui import KApplication, KIcon

        aboutData = KAboutData(
            name, #appName
            name, #catalogName
            ki18n(name), #programName
            version,
            ki18n(description), #shortDescription
            KAboutData.License_BSD, #licenseKey
            ki18n("© 2010 Massimiliano Torromeo"), #copyrightStatement
            ki18n(""), #text
            url #homePageAddress
        )
        aboutData.setBugAddress("http://github.com/mtorromeo/iosshy/issues")
        aboutData.addAuthor(
            ki18n("Massimiliano Torromeo"), #name
            ki18n("Main developer"), #task
            "massimiliano.torromeo@gmail.com" #email
        )
        aboutData.setProgramLogo(QImage(":icons/network-server.png"))

        KCmdLineArgs.init(sys.argv, aboutData)

        app = KApplication()
        app.setWindowIcon(KIcon("network-server"))

        if app.isSessionRestored():
            sys.exit(0)
    except ImportError:
        app = QApplication(sys.argv)
        app.setOrganizationName("MTSoft")
        app.setApplicationName(name)


    if QSystemTrayIcon.isSystemTrayAvailable():
        translator = QTranslator()
        qmFile = "tunneller_%s.qm" % QLocale.system().name()
        if os.path.isfile(qmFile):
            translator.load(qmFile)
        app.installTranslator(translator)

        dialog = TunnelDialog()
        sys.exit(app.exec_())
    else:
        print "System tray not available. Exiting."
        sys.exit(1)

if __name__ == "__main__":
    main()
