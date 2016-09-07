#!/usr/bin/env python
from distutils.core import setup, Extension
import setuptools


setup(
    name     = 'pyflowgraph',
    license  = 'BSD',

    description      = 'PySide/PyQt library to create nodes/graphs',

    keywords         = 'pyflowgraph node graph PySide PySide2 PyQt4 PyQt5',
    install_requires = ['six','Qt.py','PySide'],
    packages         = setuptools.find_packages(),

    zip_safe         = False,

    package_data = {
        ''         : ['*.txt', '*.rst'],
    },

    classifiers      = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Environment :: X11 Applications :: Qt'

        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
)

