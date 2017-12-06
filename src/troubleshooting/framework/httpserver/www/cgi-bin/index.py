#!/usr/bin/env python
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.running.recovery import recovery
from os.path import abspath,dirname,join
import cgi
import os,sys
from troubleshooting.framework.libraries.system import get_FileCreateTime,get_FileModifyTime,get_FileCreateTimeStamp
from troubleshooting.framework.libraries.parsexml import parsexml

form = cgi.FieldStorage()
homeDir = dirname(dirname(abspath(__file__)))



if form.has_key("Recovery"):
    #recovery mode
    ProjectDir = form.getvalue("ProjectDir").replace("/",os.path.sep)

    sys.path.append(ProjectDir)
    ConfigManagerInstance.config = {"Recovery":form.getvalue("Recovery")}
    if form.getvalue("Host") == "localhost":
        ConfigManagerInstance.config = {"Host": None}
    else:
        ConfigManagerInstance.config = {"Host": form.getvalue("Host")}
    ConfigManagerInstance.config = {"Port": form.getvalue("Port")}
    ConfigManagerInstance.config = {"User": form.getvalue("User")}
    ConfigManagerInstance.config = {"Password": form.getvalue("Password")}
    ConfigManagerInstance.config = {"__ReportHash__": form.getvalue("reportHash")}
    ConfigManagerInstance.config = {"__ProjectCWD__": form.getvalue("ProjectDir")}
    ConfigManagerInstance.config = {"R_TestPoint": form.getvalue("TestPoint") }

    if ConfigManagerInstance.config["Recovery"]:
        print "Content-Type: text/html"  # HTML is following
        print  # blank line, end of headers
        recovery(ConfigManagerInstance.config["Recovery"])




else:
    #generate mode
    if form.has_key("reportHash"):
        index_page = join(homeDir, form.getvalue("reportHash"), "index.html")

        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        try:
            with open(index_page,"rb") as f:
                print f.read()
        except IOError,e:
            error_page = join(homeDir,"others","404.html")
            with open(error_page,"rb") as f:
                print f.read()
    else:
        list_page = join(homeDir,"list.html")
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        if not form.has_key("reportHash"):
            hashlink = []
            index = []
            filepathDict = {}
            for _fileName in os.listdir(homeDir):
                if _fileName.endswith(".d"):
                    _filepath = join(homeDir,_fileName)
                    fileCreateTimeStamp = get_FileCreateTimeStamp(_filepath)
                    index.append(fileCreateTimeStamp)
                    filepathDict[str(fileCreateTimeStamp)] = _filepath
            index.sort()
            reportLines = []
            for _index in index:
                _filepath = filepathDict[str(_index)]
                _fileName = _filepath.split(os.path.sep)[-1]

                fileCreateTime = get_FileCreateTime(_filepath)
                fileModifyTime = get_FileModifyTime(_filepath)
                dataxmlpath = join(_filepath,"data.xml")
                pass_num,fail_num = parsexml().get_cases_status(dataxmlpath)
                status = "%s PASS / %s FAIL"%(pass_num,fail_num)
                url = "http://localhost:8888/www/cgi-bin/index.py?reportHash=%s"%_fileName
                reportLine = """
                	<tr>
								<td><h3><a href="%s">This is Troubleshooting Report</a></h3></td>
								<td>%s</td>
								<td><a href="%s">%s</a></td>
								<td><a href="#" class="ico del">Delete</a></td>
							</tr>
                """%(url,fileCreateTime,url,status)
                reportLines.append(reportLine)

            reportLinesStr = "\n".join(reportLines)

            try:
                with open(list_page,"rb") as f:
                    content = f.read()
                    content = content.replace("{REPORTLIST}",reportLinesStr)
                    print content
            except IOError,e:
                error_page = join(homeDir, "others", "404.html")
                with open(error_page, "rb") as f:
                    print f.read()