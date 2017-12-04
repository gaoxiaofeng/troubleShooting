# -*- coding: utf-8 -*-
from optparse import  OptionParser
import sys,os,platform,time,traceback,getpass
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.builder import BuilderFactory
from troubleshooting.framework.version.version import VERSION
from troubleshooting.framework.libraries.baseString import getRandomString
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.output.welcome import welcome
from troubleshooting.framework.libraries.system import clean
from troubleshooting.framework.modules.thread import ThreadManager
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.httpserver.server import  server
from troubleshooting.framework.output.browser import Browser
from troubleshooting.framework.remote.client import client
from troubleshooting.framework.libraries.filter import filterCaselist
from troubleshooting.framework.output.progressDialog import  ProgressDialog
from troubleshooting.framework.output.report import report
from troubleshooting.framework.output.output import OutPut
from troubleshooting.framework.running.recovery import recovery


class BaseHandle(object):
    def __init__(self):
        super(BaseHandle,self).__init__()
        self.successor = None
    def handle(self):
        if self.successor:
            self.successor.handle()
class ParseArgsHandle(BaseHandle):
    def __init__(self):
        super(ParseArgsHandle,self).__init__()
    def handle(self):
        _system_ = platform.system().lower()
        opt = OptionParser(version=VERSION)
        opt.add_option("-l", "--list", dest="List", help="print list of cases", action="store_true")
        opt.add_option("--clean", dest="Clean", help="remove all report directory", action="store_true")
        opt.add_option("--readonly", dest="readonly", help="read only mode, can only fetch reports",
                       action="store_true")
        opt.add_option("--host", dest="Host", help="host for remote connection")
        opt.add_option("--port", dest="Port", help="port for remote connection ,defaut port is 22", default="22")
        opt.add_option("--user", dest="User", help="user for remote connection , default user is root", default="root")
        # opt.add_option("--password", dest="Password", help="password for remote connection , default password is arthur", default="root")
        opt.add_option("--case", dest="case", help="select the case to run by case name")
        opt.add_option("--include", dest="include", help="""select cases to run by tag, Tags can also be combined together with  `AND` and `OR` .
            Example: --include=coolANDhot""")
        opt.add_option("--exclude", dest="exclude", help="""select cases not to run by tag. Tags can also be combined together with  `AND` and `OR` .
            Example: --include=coolORhot""")
        opt.add_option("-r", "--recovery", dest="Recovery")
        options, args = opt.parse_args()
        reportHash = (getRandomString(5) + ".d")
        reportFile = os.path.join(os.getcwd(), "www", reportHash, "report.html")
        ConfigManagerInstance.config = {"Case": options.case}
        ConfigManagerInstance.config = {"Report": reportFile}
        ConfigManagerInstance.config = {"Include": options.include}
        ConfigManagerInstance.config = {"Exclude": options.exclude}
        ConfigManagerInstance.config = {"Host": options.Host}
        ConfigManagerInstance.config = {"Port": options.Port}
        ConfigManagerInstance.config = {"User": options.User}
        ConfigManagerInstance.config = {"Password":""}
        ConfigManagerInstance.config = {"SYSTEM": _system_}
        ConfigManagerInstance.config = {"List": options.List}
        ConfigManagerInstance.config = {"Clean": options.Clean}
        ConfigManagerInstance.config = {"ReadOnly": options.readonly}
        ConfigManagerInstance.config = {"Recovery": options.Recovery}
        ConfigManagerInstance.config = {"__ReportHash__": reportHash}
        ConfigManagerInstance.config = {"__ReportName__": "report.html"}
        ConfigManagerInstance.config = {"__ProjectCWD__": os.getcwd()}

        super(ParseArgsHandle,self).handle()




class ListHandle(BaseHandle):
    def __init__(self):
        super(ListHandle,self).__init__()
    def handle(self):
        if ConfigManagerInstance.config["List"]:
            CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)
            builderfactory = BuilderFactory()
            builderfactory.getBuilder(LAYER.Case).builder()
            caseNameList = CaseManagerInstance.get_keyword()
            welcome().loadCasePrint(caseNameList)
            welcome().ListCasePrint(caseNameList)
        else:
            super(ListHandle,self).handle()

class CleanHandle(BaseHandle):
    def __init__(self):
        super(CleanHandle,self).__init__()
    def handle(self):
        if ConfigManagerInstance.config["Clean"]:
            clean()
        else:
            super(CleanHandle,self).handle()

class ReadOnlyHandle(BaseHandle):
    def __init__(self):
        super(ReadOnlyHandle,self).__init__()
    def handle(self):
        if ConfigManagerInstance.config["ReadOnly"]:
            try:
                cigServer = server(skip_deploy=True)
                ThreadManager().append(cigServer)
                cigServer.start()
                print "init ReadOnly mode successfully."
                linkage = "http://localhost:8888/www/cgi-bin/index.py"
                if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                    Browser().openLocalReport(linkage)
                else:
                    print "[Tips]:please visit the webpage %s" % linkage
            except Exception, e:
                print "Can not init ReadOnly mode."
                logger().error(traceback.format_exc())
            finally:
                while 1:
                    time.sleep(0.1)

        else:
            super(ReadOnlyHandle,self).handle()

class TestConnectionForRemoteHandle(BaseHandle):
    def __init__(self):
        super(TestConnectionForRemoteHandle,self).__init__()
    def handle(self):
        if ConfigManagerInstance.config["Host"]:
            # remote mode
            host = ConfigManagerInstance.config["Host"]
            port = ConfigManagerInstance.config["Port"]
            user = ConfigManagerInstance.config["User"]

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
            while 1:
                password = getpass.getpass("password:  ")
                if password:
                    break
            ConfigManagerInstance.config["Password"] = password
            if client().test_connection(host, port, user, password):
                super(TestConnectionForRemoteHandle,self).handle()
        else:
            super(TestConnectionForRemoteHandle,self).handle()

class DoDetectHandle(BaseHandle):
    def __init__(self):
        super(DoDetectHandle,self).__init__()
    def handle(self):
        if ConfigManagerInstance.config["Recovery"] is None:
            #   detect mode
            _startTime = time.time()
            CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)
            builderfactory = BuilderFactory()
            builderfactory.getBuilder(LAYER.KeyWords).builder()
            builderfactory.getBuilder(LAYER.TestPoint).builder()
            builderfactory.getBuilder(LAYER.Case).builder()
            OutPutThreadno = ThreadManager().start(OutPut())
            caseNameList = CaseManagerInstance.get_keyword()
            caseNameList_NeedRun = filterCaselist(caseNameList)

            caseNameListLength = len(caseNameList_NeedRun)
            if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.LINUX.value:
                # local is linux
                welcome().logo()
                welcome().loadCasePrint(caseNameList_NeedRun)
                Progress = ProgressDialog(caseNameListLength)
                Progressthreadno = ThreadManager().start(Progress)

                try:
                    for i, caseName in enumerate(caseNameList_NeedRun):
                        Progress.set(i)
                        behavior = CaseManagerInstance.run_case(caseName)
                        Progress.set(i + 1)
                        if behavior == BEHAVIOR.EXIT:
                            break
                except Exception, e:
                    traceback.print_exc()
                    ThreadManager().stop(Progressthreadno)

                else:
                    ThreadManager().join(Progressthreadno)
                    report().console()
                    report().writeReport()
                finally:
                    ThreadManager().join(Progressthreadno)
                    ThreadManager().stop(OutPutThreadno)
            elif ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                try:
                    welcome().logo()
                    welcome().loadCasePrint(caseNameList_NeedRun)
                    for caseName in caseNameList_NeedRun:
                        behavior = CaseManagerInstance.run_case(caseName)
                        if behavior == BEHAVIOR.EXIT:
                            break
                    report().writeReport()
                except Exception, e:
                    traceback.print_exc()
                finally:
                    ThreadManager().stop(OutPutThreadno)
            else:
                print "unsupport system %s" % ConfigManagerInstance.config["SYSTEM"]
            _endTime = time.time()
            print "Total cost time: %.3f s" % (_endTime - _startTime)
            if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                try:
                    ThreadManager().start(server())
                    reportHash = ConfigManagerInstance.config["__ReportHash__"]
                    Browser().openLocalReport("http://localhost:8888/www/cgi-bin/index.py?reportHash=%s" % reportHash)
                except Exception, e:
                    print "Report save as %s" % ConfigManagerInstance.config["Report"]
                    logger().error(traceback.format_exc())
                finally:
                    while 1:
                        time.sleep(0.1)
            else:
                print "Report save as %s" % ConfigManagerInstance.config["Report"]


class DoRecoveryHandle(BaseHandle):
    def __init__(self):
        super(DoRecoveryHandle,self).__init__()
    def handle(self):
        #recovery mode
        if ConfigManagerInstance.config["Recovery"]:
            recovery(ConfigManagerInstance.config["Recovery"])
        else:
            super(DoRecoveryHandle,self).handle()


class ArgsHandleClient(object):
    def __init__(self):
        super(ArgsHandleClient,self).__init__()
    def handle(self):
        h0 = ParseArgsHandle()
        h1 = ListHandle()
        h2 = CleanHandle()
        h3 = ReadOnlyHandle()
        h4 = TestConnectionForRemoteHandle()
        h5 = DoDetectHandle()
        h6 = DoRecoveryHandle()
        h0.successor = h1
        h1.successor = h2
        h2.successor = h3
        h3.successor = h4
        h4.successor = h5
        h5.successor = h6
        h0.handle()





