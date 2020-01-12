#!/usr/bin/env python
# -*- coding: utf-8 -*-

# example file using pyteetime, the python version of unix tee

# This program is free software: you can use and distribute it under the
# terms of the GPL v2 or, at your option, any later GPL version:
# http://www.gnu.org/licenses/

##############################################################################

if __name__ == '__main__':

    from pyteetime import tee
    import sys

    print('This prologue will appear on screen but not in a logfile')
    
    LOGFILE = tee.stdout_start(append=False) # STDOUT
    # from now on, all output is also copied to the logfile

    tee.stderr_start(append=False) # STDERR
    # from now on, all output to STDERR is also copied to tee-test.err

    print('This text will appear on screen and also in the logfile')

    print('This will appear on screen and also in tee-test.err', file=sys.stderr) 

    # input from keyboard does not go to logfile:
    answer = input('Enter something!\n')

    # show the input to make sure it also goes into the logfile:
    print('The user typed: %s' % (answer))

    # data written to a file is not copied to the logfile:
    DATAFILE = open('tee-test.dat','w+')
    print(list(range(5)), file=DATAFILE)
    DATAFILE.close()

    print('This goes to the logfile but will not appear on screen', file=LOGFILE)

    tee.stdout_stop()
    # from now on, output to STDOUT will not go to tee-test.log anymore

    tee.stderr_stop()
    # from now on, output to STDERR will not go to tee-test.err anymore

    print('This epilogue will appear on screen but not in a logfile')

##############################################################################
