# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.builder import BuilderFactory
from troubleshooting.framework.output.output import OutPut
from troubleshooting.framework.output.welcome import welcome
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.version.version import VERSION
from optparse import OptionParser
from troubleshooting.framework.output.progressDialog import  ProgressDialog
from troubleshooting.framework.output.report import report
import traceback
from troubleshooting.framework.output.Print import *
from troubleshooting.framework.output.browser import Browser
from troubleshooting.framework.remote.client import client
from troubleshooting.framework.libraries.library import getRandomString,isSublist,compareList,parseRecoveryArgs
from troubleshooting.framework.libraries.system import clean
from troubleshooting.framework.log.logger import logger
import platform
import sys,os
import time
import signal
sys.path.append(os.getcwd())
def onsignal_int(a,b):
    global PD
    try:
        PD.stop()
    except:
        pass
    finally:
        OutPut().stop()
    print '\nExit'
    sys.exit(0)
signal.signal(signal.SIGINT, onsignal_int)

#Logger = logger()
def run_cli(*args):
    global PD
    _startTime = time.time()
    _system_ =  platform.system().lower()
    opt = OptionParser(version=VERSION)
    opt.add_option("-l","--list", dest="List", help="print list of cases",action="store_true")
    opt.add_option("--clean", dest="Clean", help="remove all report directory", action="store_true")
    opt.add_option("--host",dest="Host",help="host for remote connection")
    opt.add_option("--port",dest="Port",help="port for remote connection ,defaut port is 22",default=22)
    opt.add_option("--user", dest="User", help="user for remote connection , default user is root", default="root")
    opt.add_option("--password", dest="Password", help="password for remote connection , default password is arthur", default="arthur")
    opt.add_option("--case",dest="case",help="select the case to run by case name")
    opt.add_option("--include",dest="include",help="""select cases to run by tag, Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolANDhot""")
    opt.add_option("--exclude",dest="exclude",help="""select cases not to run by tag. Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolORhot""")
    opt.add_option("--report",dest="report",help="HTML report file, default is report.html",default="report.html")
    opt.add_option("-r","--recovery", dest="recovery", help="try to recovery problem")
    options, args = opt.parse_args()
    reportFile = os.path.join((getRandomString(5) + ".d"),options.report)
    ConfigManagerInstance.config = {"Case":options.case}
    ConfigManagerInstance.config = {"Report":reportFile}
    ConfigManagerInstance.config = {"Include":options.include}
    ConfigManagerInstance.config = {"Exclude":options.exclude}
    ConfigManagerInstance.config = {"Host":options.Host}
    ConfigManagerInstance.config = {"Port":options.Port}
    ConfigManagerInstance.config = {"User":options.User}
    ConfigManagerInstance.config = {"Password":options.Password}
    ConfigManagerInstance.config = {"SYSTEM":_system_}
    if options.List:
        CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)
        builderfactory = BuilderFactory()
        # builderfactory.getBuilder(LAYER.KeyWords).builder()
        # builderfactory.getBuilder(LAYER.TestPoint).builder()
        builderfactory.getBuilder(LAYER.Case).builder()
        caseNameList = CaseManagerInstance.get_keyword()
        welcome()
        welcome().loadCasePrint(caseNameList)
        welcome().ListCasePrint(caseNameList)
        return
    if options.Clean:
        clean()
        return
    if options.Host:
        #remote mode
        host = options.Host
        port = options.Port
        user = options.User
        password = options.Password
        if user != "root":
            print "WARN: Access right is not enough."
        try:
            port = int(port)
        except:
            raise Exception("port must be int type")
        if not host:
            raise Exception("host is mandatory")
        if not port:
            raise Exception("port is mandatory")
        if not user:
            raise Exception("user is mandatory")
        if not password:
            raise Exception("password is mandatory")

        if not client().test_connection(host,port,user,password):
            return

    if options.recovery is None:
        # redirection()
        # print "current system is %s" % _system_
        CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)

        builderfactory = BuilderFactory()
        builderfactory.getBuilder(LAYER.KeyWords).builder()
        builderfactory.getBuilder(LAYER.TestPoint).builder()
        builderfactory.getBuilder(LAYER.Case).builder()

        OutPut().start()
        caseNameList = CaseManagerInstance.get_keyword()
        caseNameListLength = len(caseNameList)
        if _system_ == SYSTEM.LINUX.value:
            welcome()
            welcome().logo()
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
        elif _system_ == SYSTEM.WINDOWS.value:
            try:
                welcome()
                welcome().logo()
                welcome().loadCasePrint(caseNameList)
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
        _endTime = time.time()
        print "Total cost time: %.3f s"%(_endTime-_startTime)
        if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
            try:
                Browser().openLocalReport(ConfigManagerInstance.config["Report"])
            except:
                print "Report save as %s"%ConfigManagerInstance.config["Report"]
        else:
            print "Report save as %s" % ConfigManagerInstance.config["Report"]
    if options.recovery:
        recoverSteps = parseRecoveryArgs(options.recovery)
        recoverStepsName = [step["method"] for step in recoverSteps]
        RecoveryManagerInstance = ManagerFactory().getManager(LAYER.Recovery)
        builderfactory = BuilderFactory()
        builderfactory.getBuilder(LAYER.Recovery).builder()
        recoveryList = RecoveryManagerInstance.get_keyword()


        if isSublist(recoveryList,recoverStepsName):
            print "Framework: try to fix problem."
            for i,step in enumerate(recoverSteps):
                stepName = step["method"]
                stepArgs = step["args"].split(";")
                sys.stdout.write("Framework: step %s.  %20s"%(i+1,stepName))
                sys.stdout.flush()
                try:
                    status = RecoveryManagerInstance.run_recovery(stepName,*stepArgs)
                except Exception,e:
                    logger().error(traceback.format_exc())
                    status = STATUS.FAIL
                    sys.stdout.write("\t[%s]\n" %status)
                    sys.stdout.flush()
                    print "Framework: ERROR message save in log file."
                else:
                    sys.stdout.write("\t[%s]\n"%status)
                    sys.stdout.flush()
                finally:
                    if status == STATUS.FAIL:
                        print "Framework: recovery failed!"
                        return
            print "Framework: recovery successfully!"

        else:
            print "Framework: unkown recovery steps : %s"%compareList(recoveryList,recoverStepsName)



if __name__ == "__main__":
    run_cli(sys.argv[1:])