#!/usr/bin/env python
# -*- coding: utf-8 -*- Time-stamp: <2017-06-29 16:07:53 sander>*-

# pyteetime: python version of unix tee
# Version: 0.9
# http://www.rolf-sander.net/software/pyteetime

# Based on original code from Akkana Peck, see
# http://shallowsky.com/blog/programming/python-tee.html
# Classmethods added by Rolf Sander, 2017

# This program is free software: you can use and distribute it under the
# terms of the GPL v2 or, at your option, any later GPL version:
# http://www.gnu.org/licenses/

##############################################################################

import sys

class tee(object):
    """ tee for python
    """
    def __init__(cls, _fd1, _fd2):
        cls.fd1 = _fd1
        cls.fd2 = _fd2
    def __del__(cls):
        if ((cls.fd1 != sys.stdout) and (cls.fd1 != sys.stderr)):
            cls.fd1.close()
        if ((cls.fd2 != sys.stdout) and (cls.fd2 != sys.stderr)):
            cls.fd2.close()
    def write(cls, text):
        cls.fd1.write(text)
        cls.fd2.write(text)
    def flush(cls):
        cls.fd1.flush()
        cls.fd2.flush()

    # STDOUT:
    @classmethod
    def stdout_start(cls, logfilename='stdout.log', append=True):
        cls.stdoutsav = sys.stdout
        if (append):
            cls.LOGFILE = open(logfilename, 'a')
        else:
            cls.LOGFILE = open(logfilename, 'w')
        sys.stdout = tee(cls.stdoutsav, cls.LOGFILE)
        return cls.LOGFILE
    @classmethod
    def stdout_stop(cls):
        cls.LOGFILE.close()
        sys.stdout = cls.stdoutsav

    # STDERR:
    @classmethod
    def stderr_start(cls, errfilename='stderr.log', append=True):
        cls.stderrsav = sys.stderr
        if (append):
            cls.ERRFILE = open(errfilename, 'a')
        else:
            cls.ERRFILE = open(errfilename, 'w')
        sys.stderr = tee(cls.stderrsav, cls.ERRFILE)
        return cls.ERRFILE
    @classmethod
    def stderr_stop(cls):
        cls.ERRFILE.close()
        sys.stderr = cls.stderrsav

##############################################################################
