from troubleshooting.framework.output.output import OutPut
from troubleshooting.framework.version.version import VERSION
from optparse import OptionParser
import os,sys
import signal
import platform
import time
from troubleshooting.framework.management.client import client
def onsignal_int(a,b):
    OutPut().stop()
    print '\nExit'
    sys.exit(0)
signal.signal(signal.SIGINT, onsignal_int)


def run_cli(*args):
    client().handle(*args)

if __name__ == "__main__":
    run_cli(sys.argv[1:])