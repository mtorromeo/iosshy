#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
py2app/py2exe build script for IOSSHy

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

# Include iosshy application first to force sip api version 2
from iosshy import application
import sys, os
from setuptools import setup
#from distutils.core import setup

mainscript = 'bin/iosshy'
README = os.path.join(os.path.dirname(__file__), 'README.rst')

# Programmatically compile the forms with the uic module, sadly this is not possible for icon resources
from PyQt4 import uic
for form in ("tunneldialog.ui",):
	uif = "Ui_{0}.py".format( form.rpartition('.')[0] )
	with open(os.path.join("iosshy", uif), "wb") as f:
		uic.compileUi(os.path.join("iosshy", form), f)

if sys.platform == 'darwin':
	extra_options = dict(
		setup_requires=['py2app'],
		app=[mainscript],
		options={"py2app": {
			"argv_emulation": True,
			"includes": ["sip", "PyQt4.QtCore", "PyQt4.QtGui"]
		}},
	)
elif sys.platform == 'win32':
	import py2exe

	# Override isSystemDLL function to force inclusion of msvcp90.dll
	origIsSystemDLL = py2exe.build_exe.isSystemDLL
	def isSystemDLL(pathname):
		if os.path.basename(pathname).lower() == "msvcp90.dll":
			return 0
		return origIsSystemDLL(pathname)
	py2exe.build_exe.isSystemDLL = isSystemDLL

	extra_options = dict(
		windows=[{
			"script": mainscript,
			"icon_resources": [(0, "iosshy.ico")]
		}],
		options={"py2exe": {
			"optimize": 2,
			"skip_archive": True,
			"includes": ["sip"]
		}}
	)
else:
	extra_options = {}

setup(
	name = application.name,
	packages = ["iosshy"],
	scripts = [mainscript],
	requires = ["paramiko", "keyring", "setproctitle"],
	version = application.version,
	description = application.description,
	long_description = open(README).read(),
	author = "Massimiliano Torromeo",
	author_email = "massimiliano.torromeo@gmail.com",
	url = application.url,
	download_url = "http://github.com/mtorromeo/iosshy/tarball/v"+application.version,
	keywords = ["qt", "pyqt", "desktop", "ssh"],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: BSD License",
		"Environment :: X11 Applications :: Qt",
		"Intended Audience :: System Administrators",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: POSIX :: Linux",
		"Operating System :: POSIX :: BSD",
		"Natural Language :: English",
		"Topic :: System :: Monitoring",
		"Topic :: Utilities"
	],
	license = "BSD License",
	**extra_options
)
