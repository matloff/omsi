__author__ = 'rylan'


import sys

try:
    import hashlib
except ImportError:
    print 'Cannot import hashlib. Exiting...'
    sys.exit()

# default filename is Checksum.py.  Remove later
def checksum(filename = 'Checksum.py'):

    # save file contents
    stream = open(filename, 'r').read()

    # compute secure hash of file contents
    h = hashlib.sha256(stream)

    # return hash in hexadecimal
    return h.hexdigest()
