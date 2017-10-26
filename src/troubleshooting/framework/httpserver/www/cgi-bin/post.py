#!/usr/bin/env python
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.running.recovery import recovery
from os.path import abspath,dirname,join
import cgi
import os,sys

form = cgi.FieldStorage()
homeDir = dirname(dirname(abspath(__file__)))



if form.has_key("recovery"):
    #recovery mode


    args = form.getvalue("recovery")
    args = eval(args)
    sys.path.append(args["ProjectDir"])
    ConfigManagerInstance.config = {"Recovery":args["Recovery"]}
    ConfigManagerInstance.config = {"Host": args["Host"]}
    ConfigManagerInstance.config = {"Port": args["Port"]}
    ConfigManagerInstance.config = {"User": args["User"]}
    ConfigManagerInstance.config = {"Password": args["Password"]}

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

        with open(index_page,"rb") as f:
            print f.read()
    else:
        print "Content-Type: text/html"     # HTML is following
        print                               # blank line, end of headers
        print "<h>Error:    args `reportHash` and  `reportName` are  mandatory!</h>"