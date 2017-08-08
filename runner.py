import sys
from framework.configuration import  ConfigManagerInstance
from framework.variable.variable import *
from framework.builder import BuilderFactory
# from framework.log.logger import logger
from framework.output.output import OutPut
from framework.output.welcome import welcome
from framework.manager import ManagerFactory
# import time
import signal
from  optparse import OptionParser
from framework.output.welcome import  ProgressDialog
from framework.output.report import report
import traceback
from framework.output.Print import *
import platform

def onsignal_int(a,b):
    OutPut().stop()
    print '\nExit'
    sys.exit(0)
signal.signal(signal.SIGINT, onsignal_int)

#Logger = logger()
if __name__ == "__main__":
    _system_ =  platform.system().lower()
    print "current system is %s"%_system_
    parser = OptionParser()
    parser.add_option("-m",dest="runMode",help="support simple/detail,default is simple",default="simple")
    options, args = parser.parse_args()
    ConfigManagerInstance.config = {"runMode":DetailMode if options.runMode == "detail" else SingleMode}
    CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)

    builderfactory = BuilderFactory()
    builderfactory.getBuilder(LAYER.KeyWords).builder()
    builderfactory.getBuilder(LAYER.TestPoint).builder()
    builderfactory.getBuilder(LAYER.Case).builder()

    OutPut().start()
    caseNameList = CaseManagerInstance.get_keyword()
    caseNameListLength = len(caseNameList)
    if _system_ == SYSTEM.LINUX:
        welcome()
        welcome().loadCasePrint(caseNameList)
        PD = ProgressDialog(caseNameListLength)
        PD.start()
        try:

            for i,caseName in enumerate(caseNameList):
                # i += 1
                PD.set(i)
                behavior =  CaseManagerInstance.run_case(caseName)
                PD.set(i+1)
                if behavior == BEHAVIOR.EXIT:
                    break
        except Exception,e:
            traceback.print_exc()
            PD.stop()

        else:
            while 1:
                #wait for PD thread exit
                if PD.is_alive() is False:
                    break
            report().console()
            report().writeReport()
        finally:
            while 1:
                #wait for PD thread exit
                if PD.is_alive() is False:
                    break
            OutPut().stop()
    elif _system_ == SYSTEM.WINDOWS:
        try:

            for caseName in caseNameList:
                behavior =  CaseManagerInstance.run_case(caseName)
                if behavior == BEHAVIOR.EXIT:
                    break
            report().writeReport()
        except Exception,e:
            traceback.print_exc()
        finally:
            OutPut().stop()
    else:
        print "unsupport system %s"%_system_
