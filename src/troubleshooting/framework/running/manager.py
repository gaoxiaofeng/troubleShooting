from troubleshooting.framework.output.output import OutPut
import os,sys
import signal
from troubleshooting.framework.management.client import client
from troubleshooting.framework.libraries.signal import onsignal_int
signal.signal(signal.SIGINT, onsignal_int)


def run_cli(*args):
    client().handle(*args)

if __name__ == "__main__":
    run_cli(sys.argv[1:])