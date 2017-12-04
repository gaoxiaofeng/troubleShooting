# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.thread import ThreadManager
import sys

def onsignal_int(a,b):
    print "\nExiting..."
    ThreadManager().stop_all()
    ThreadManager().join_all()
    print '\nExited'
    sys.exit(0)