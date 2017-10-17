#!/usr/bin/env python
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.running.recovery import recovery
from os.path import abspath,dirname,join
import cgi
import os,sys

form = cgi.FieldStorage()
if form.has_key("reportHash") and form.has_key("reportName"):
    homeDir = dirname(dirname(abspath(__file__)))
    index_page = join(homeDir,form.getvalue("reportHash"),form.getvalue("reportName"))
    # Output to stdout, CGIHttpServer will take this as response to the client
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

    with open(index_page,"rb") as f:
        print f.read()

if form.has_key("recovery"):
    args = form.getvalue("recovery")
    args = eval(args)
    # os.chdir(args["CWD"])
    sys.path.append(args["ProjectDir"])
    ConfigManagerInstance.config = {"Recovery":args["Recovery"]}
    ConfigManagerInstance.config = {"Host": args["Host"]}
    ConfigManagerInstance.config = {"Port": args["Port"]}
    ConfigManagerInstance.config = {"User": args["User"]}
    ConfigManagerInstance.config = {"Password": args["Password"]}
    if ConfigManagerInstance.config["Recovery"]:
        print "Content-Type: text/html"  # HTML is following
        print  # blank line, end of headers
        # print "CWD",os.getcwd()
        # print ConfigManagerInstance.config

        recovery(ConfigManagerInstance.config["Recovery"])
        print "recovery successfully"

