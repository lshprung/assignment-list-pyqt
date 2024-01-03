#!/usr/bin/env python3
from setuptools import setup

# For getting a git snapshot: ./setup.py egg_info -b "+git`date '+%Y%m%d'`" build sdist
# For building on Windows: [/PATH/TO/]pyinstaller.exe --icon=data\assignment-list.ico -w --add-data=assignment_list_pyqt:assignment_list_pyqt assignment-list
setup()
