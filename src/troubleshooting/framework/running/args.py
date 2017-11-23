from optparse import  OptionParser
from troubleshooting.framework.version.version import VERSION
from troubleshooting.framework.libraries.library import getRandomString,isSublist,compareList,parseRecoveryArgs
import sys,os,platform
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
def parsedArgs():
    _system_ = platform.system().lower()
    opt = OptionParser(version=VERSION)
    opt.add_option("-l","--list", dest="List", help="print list of cases",action="store_true")
    opt.add_option("--clean", dest="Clean", help="remove all report directory", action="store_true")
    opt.add_option("--readonly",dest="readonly",help="read only mode, can only fetch reports",action="store_true")
    opt.add_option("--host",dest="Host",help="host for remote connection")
    opt.add_option("--port",dest="Port",help="port for remote connection ,defaut port is 22",default="22")
    opt.add_option("--user", dest="User", help="user for remote connection , default user is root", default="root")
    opt.add_option("--password", dest="Password", help="password for remote connection , default password is arthur", default="arthur")
    opt.add_option("--case",dest="case",help="select the case to run by case name")
    opt.add_option("--include",dest="include",help="""select cases to run by tag, Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolANDhot""")
    opt.add_option("--exclude",dest="exclude",help="""select cases not to run by tag. Tags can also be combined together with  `AND` and `OR` .
    Example: --include=coolORhot""")
    # opt.add_option("--report",dest="report",help="HTML report file, default is report.html",default="report.html")
    # opt.add_option("-r","--recovery", dest="Recovery", help="try to recovery problem")
    opt.add_option("-r", "--recovery", dest="Recovery")
    options, args = opt.parse_args()
    reportHash = (getRandomString(5) + ".d")
    reportFile = os.path.join(os.getcwd(),"www",reportHash,"report.html")
    ConfigManagerInstance.config = {"Case":options.case}
    ConfigManagerInstance.config = {"Report":reportFile}
    ConfigManagerInstance.config = {"Include":options.include}
    ConfigManagerInstance.config = {"Exclude":options.exclude}
    ConfigManagerInstance.config = {"Host":options.Host}
    ConfigManagerInstance.config = {"Port":options.Port}
    ConfigManagerInstance.config = {"User":options.User}
    ConfigManagerInstance.config = {"Password":options.Password}
    ConfigManagerInstance.config = {"SYSTEM":_system_}
    ConfigManagerInstance.config = {"List":options.List}
    ConfigManagerInstance.config = {"Clean": options.Clean}
    ConfigManagerInstance.config = {"ReadOnly":options.readonly}
    ConfigManagerInstance.config = {"Recovery": options.Recovery}
    ConfigManagerInstance.config = {"__ReportHash__": reportHash}
    ConfigManagerInstance.config = {"__ReportName__": "report.html"}
    ConfigManagerInstance.config = {"__ProjectCWD__": os.getcwd()}