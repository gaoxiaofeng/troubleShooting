# -*- coding: utf-8 -*-
from framework.modules.configuration import  ConfigManagerInstance
from framework.variable.variable import *
from framework.modules.builder import BuilderFactory
from framework.output.output import OutPut
from framework.output.welcome import welcome
from framework.modules.manager import ManagerFactory
import time
import signal
from optparse import OptionParser
from framework.output.progressDialog import  ProgressDialog
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
    _startTime = time.time()
    _system_ =  platform.system().lower()
    version = "1.0.1"
    opt = OptionParser(version=version)

    opt.add_option("--host",dest="Host",help="host for remote connection")
    opt.add_option("--port",dest="Port",help="port for remote connection ,defaut port is 22",default=22)
    opt.add_option("--user", dest="User", help="user for remote connection , default user is root", default="root")
    opt.add_option("--password", dest="Password", help="password for remote connection , default password is arthur", default="arthur")
    opt.add_option("--sync",dest="sync",help="yes/no,default is yes",default="yes")
    opt.add_option("--console", dest="console", help="set console to on/off,default is on", default="on")
    opt.add_option("--name",dest="name",help="select the case to run by name")
    opt.add_option("--include",dest="include",help="""select cases to run by tag, Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolANDhot""")
    opt.add_option("--exclude",dest="exclude",help="""select cases not to run by tag. Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolORhot""")
    opt.add_option("--report",dest="report",help="HTML report file, default is report.html",default="report.html")

    options, args = opt.parse_args()

    ConfigManagerInstance.config = {"Console":True if options.console == "on" else False}
    ConfigManagerInstance.config = {"Sync":True if options.sync == "yes" else False}
    ConfigManagerInstance.config = {"Name":options.name}
    ConfigManagerInstance.config = {"Report":options.report}
    ConfigManagerInstance.config = {"Include":options.include}
    ConfigManagerInstance.config = {"Exclude":options.exclude}
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
        from framework.remote.remote import Remote
        remote = Remote()
        remote.open_connection(host,port=port, username=user, password=password)
        remote.remoteRunning()
        remote.close_connection()
        _endTime = time.time()
        print "Total cost time: %.3f s"%(_endTime-_startTime)
    else:
        redirection()
        print "current system is %s" % _system_
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
