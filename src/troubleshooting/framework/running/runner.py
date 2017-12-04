# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.signal import onsignal_int
from troubleshooting.framework.running.args import ArgsHandleClient
import sys,os
import signal
sys.path.append(os.getcwd())

def run_cli(*args):
    signal.signal(signal.SIGINT, onsignal_int)
    ArgsHandleClient().handle()

if __name__ == "__main__":
    run_cli(sys.argv[1:])