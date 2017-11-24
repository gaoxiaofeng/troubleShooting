# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.builder import BuilderFactory
from troubleshooting.framework.output.output import OutPut
from troubleshooting.framework.output.welcome import welcome
from troubleshooting.framework.modules.manager import ManagerFactory
# from troubleshooting.framework.version.version import VERSION
from optparse import OptionParser
from troubleshooting.framework.output.progressDialog import  ProgressDialog
from troubleshooting.framework.output.report import report
import traceback
from troubleshooting.framework.output.Print import *
from troubleshooting.framework.output.browser import Browser
from troubleshooting.framework.remote.client import client
# from troubleshooting.framework.libraries.library import getRandomString,isSublist,compareList,parseRecoveryArgs
from troubleshooting.framework.libraries.system import clean
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.httpserver.server import  server
from troubleshooting.framework.running.recovery import recovery
from troubleshooting.framework.running.args import parsedArgs
from troubleshooting.framework.libraries.filter import filterCaselist
import platform
import sys,os
import time
import signal
sys.path.append(os.getcwd())
threandList = []
def onsignal_int(a,b):
    global threandList

    for th in threandList:
        try:
            th.stop()
        except Exception, e:
            logger().error(traceback.format_exc())
        finally:
            while 1:
                time.sleep(0.1)
                if not th.isAlive():
                    break

    OutPut().stop()
    print '\nExit'
    sys.exit(0)
signal.signal(signal.SIGINT, onsignal_int)

#Logger = logger()
def run_cli(*args):
    global threandList
    _startTime = time.time()
    parsedArgs()
    if ConfigManagerInstance.config["List"]:
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
    if ConfigManagerInstance.config["Clean"]:
        clean()
        return
    if ConfigManagerInstance.config["ReadOnly"]:
        try:
            cigServer = server(skip_deploy = True)
            threandList.append(cigServer)
            cigServer.start()
            print "init ReadOnly mode successfully."
            linkage = "http://localhost:8888/www/cgi-bin/index.py"
            if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                Browser().openLocalReport(linkage)
            else:
                print "[Tips]:please visit the webpage %s"%linkage
        except Exception,e:
            print "Can not init ReadOnly mode."
            logger().error(traceback.format_exc())
        finally:
            while 1:
                time.sleep(0.1)

        return
    if ConfigManagerInstance.config["Host"]:
        #remote mode
        host = ConfigManagerInstance.config["Host"]
        port = ConfigManagerInstance.config["Port"]
        user = ConfigManagerInstance.config["User"]
        password = ConfigManagerInstance.config["Password"]
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

    if ConfigManagerInstance.config["Recovery"] is None:
        # redirection()
        # print "current system is %s" % _system_
        CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)

        builderfactory = BuilderFactory()
        builderfactory.getBuilder(LAYER.KeyWords).builder()
        builderfactory.getBuilder(LAYER.TestPoint).builder()
        builderfactory.getBuilder(LAYER.Case).builder()

        OutPut().start()
        caseNameList = CaseManagerInstance.get_keyword()
        caseNameList_NeedRun = filterCaselist(caseNameList)

        caseNameListLength = len(caseNameList_NeedRun)
        if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.LINUX.value:
            welcome()
            welcome().logo()
            welcome().loadCasePrint(caseNameList_NeedRun)
            PD = ProgressDialog(caseNameListLength)
            PD.start()
            threandList.append(PD)

            try:
                for i,caseName in enumerate(caseNameList_NeedRun):
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
        elif ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
            try:
                welcome()
                welcome().logo()
                welcome().loadCasePrint(caseNameList_NeedRun)
                for caseName in caseNameList_NeedRun:
                    behavior =  CaseManagerInstance.run_case(caseName)
                    if behavior == BEHAVIOR.EXIT:
                        break
                report().writeReport()
            except Exception,e:
                traceback.print_exc()
            finally:
                OutPut().stop()
        else:
            print "unsupport system %s"%ConfigManagerInstance.config["SYSTEM"]
        _endTime = time.time()
        print "Total cost time: %.3f s"%(_endTime-_startTime)
        if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
            try:
                cigServer = server()
                threandList.append(cigServer)
                cigServer.start()
                reportHash = ConfigManagerInstance.config["__ReportHash__"]
                Browser().openLocalReport("http://localhost:8888/www/cgi-bin/index.py?reportHash=%s"%reportHash)
            except Exception,e:
                print "Report save as %s"%ConfigManagerInstance.config["Report"]
                logger().error(traceback.format_exc())
            finally:
                while 1:
                    time.sleep(0.1)
        else:
            print "Report save as %s" % ConfigManagerInstance.config["Report"]

    if ConfigManagerInstance.config["Recovery"]:
        recovery(ConfigManagerInstance.config["Recovery"])



if __name__ == "__main__":
    run_cli(sys.argv[1:])