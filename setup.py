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
from iosshy import application
import sys, os
from setuptools import setup, find_packages

mainscript = 'bin/iosshy'
README = os.path.join(os.path.dirname(__file__), 'README.rst')

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
	extra_options = dict(
		scripts=[mainscript],
		packages = find_packages()
	)

setup(
	name=application.name,
	version=application.version,
	description=application.description,
	long_description=open(README).read(),
	keywords='qt ssh tunnel',
	author="Massimiliano Torromeo",
	author_email="massimiliano.torromeo@gmail.com",
	url=application.url,
	license="MIT License",
	**extra_options
)