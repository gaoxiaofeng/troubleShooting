import sys
from variable.variable import *
from builder import TestPointBuilder,EngineBuilder,CaseBuilder
from manager import CaseManagerInstance
from log.logger import logger
from output.output import OutPut
from output.welcome import welcome
from configuration import  ConfigManagerInstance
import time
import signal
from  optparse import OptionParser
from library.library import  ProgressDialog
from output.report import report

def onsignal_int(a,b):
    OutPut().stop()
    print '\nExit'
    sys.exit(0)
signal.signal(signal.SIGINT, onsignal_int)

#Logger = logger()
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-m",dest="runMode",help="support simple/detail,default is simple",default="simple")
    options, args = parser.parse_args()
    ConfigManagerInstance.config = {"runMode":DetailMode if options.runMode == "detail" else SingleMode}

    welcome()

    TestPointBuilder().builder()
    EngineBuilder().builder()
    CaseBuilder().builder()
    OutPut().start()
    caseNameList = CaseManagerInstance.get_keyword()
    caseNameListLength = len(caseNameList)
    welcome().loadCasePrint(caseNameList)
    PD = ProgressDialog(caseNameListLength)
    PD.start()
    i = 0
    for caseName in caseNameList:
        PD.set(i)
        i += 1
        behavior =  CaseManagerInstance.run_case(caseName)
        PD.set(i)
        if behavior == EXIT:
            break
        time.sleep(2)
    report().write()
    OutPut().stop()

