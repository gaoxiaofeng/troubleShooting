import sys
from variable.variable import *
from builder import TestPointBuilder,EngineBuilder,CaseBuilder
from manager import CaseManagerInstance
from log.logger import logger
from output.output import OutPut
import time
import signal
TestPointBuilder().builder()
EngineBuilder().builder()
CaseBuilder().builder()
OutPut().start()
def onsignal_int(a,b):
    OutPut().stop()
    print '\nExit'
    sys.exit(0)

signal.signal(signal.SIGINT,onsignal_int)
Logger = logger()
for caseName in CaseManagerInstance.get_keyword():
    _,behavior =  CaseManagerInstance.run_case(caseName)
    if behavior == EXIT:
        break
OutPut().stop()
