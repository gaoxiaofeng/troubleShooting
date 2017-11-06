#!/usr/bin/env python
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.running.recovery import recovery
from os.path import abspath,dirname,join
import cgi
import os,sys

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
    if form.has_key("reportHash") and form.has_key("reportName"):
        index_page = join(homeDir, form.getvalue("reportHash"), form.getvalue("reportName"))

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
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        error_page = join(homeDir, "others", "404.html")
        with open(error_page, "rb") as f:
            print f.read()