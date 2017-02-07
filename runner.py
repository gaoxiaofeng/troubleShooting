import sys
from variable.variable import *
from builder import TestPointBuilder,EngineBuilder,CaseBuilder
from manager import CaseManagerInstance
from log.logger import logger
from output.output import OutPut
from configuration import  ConfigManagerInstance
import time
import signal
from  optparse import OptionParser
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
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-m",dest="runMode",help="support simple/detail,default is simple",default="simple")
    options, args = parser.parse_args()
    ConfigManagerInstance.config = {"runMode":DetailMode if options.runMode == "detail" else SingleMode}
    for caseName in CaseManagerInstance.get_keyword():
        _,behavior =  CaseManagerInstance.run_case(caseName)
        if behavior == EXIT:
            break
    OutPut().stop()
