#!/usr/bin/env python2
"""
Name :          runtests.py
Created :       Sept 17 2016
Author :        Will Pittman
Contact :       willjpittman@gmail.com
________________________________________________________________________________
Description :   triggers unittests in a variety of different environments.

                All CLI arguments passed to this script are repeated
                for each call to `nosetests`.

                This script takes advantage of Qt.py's `QT_PREFERRED_BINDING`
                environment variable - which sets the Qt providing library
                that Qt.py should use. (ImportError if not available)
________________________________________________________________________________
"""
import os
import sys
import shlex
import subprocess

## ensure user has all modules required
import nose
import mock



def print_testversion( python_ver, qt_module ):
    teststr = ('-------- {python_ver}: qt_module:{qt_module} -----------'.format(**locals()))
    print( '-' * len(teststr) )
    print( teststr )
    print( '-' * len(teststr) )
    print( '\n' )


scriptdir = os.path.dirname( os.path.realpath(__file__) )

## all CLI arguments are passed to nosetests command (ex: --rednose)
args   = sys.argv

## python versions, and QtModules to test with
environments = {
    'python2':{
        'interpreter': 'python2',
        'qt_modules' : ['PyQt4','PyQt5','PySide'],
    },
    'python3':{
        'interpreter': 'python3',
        'qt_modules' : ['PyQt4','PyQt5','PySide'],
    },
}




## run tests in each environment
for env in environments:
    for qt_module in environments[ env ]['qt_modules']:
        interpreter = environments[ env ]['interpreter']

        print_testversion( env, qt_module )

        testcmd = [ interpreter, '-m', 'nose' ]
        testcmd.extend( args[1:] )
        testenv = os.environ.copy()
        testenv.update({'QT_PREFERRED_BINDING':qt_module})

        subprocess.call( testcmd, env=testenv )



