import BaseHTTPServer,CGIHTTPServer
from threading import  Thread
import os
from os.path import abspath,dirname,join
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.libraries.system import createDir,copyFile
class server(Thread):
    def __init__(self):
        super(server,self).__init__()
        self.server = None
        self.home = dirname(abspath(__file__))
    def run(self,port=8888):
        # self.copy_report_to_home()
        self.deploy_cgi()
        # os.chdir(self.home)
        self.server = BaseHTTPServer.HTTPServer(("",port), CGIHTTPServer.CGIHTTPRequestHandler)
        self.server.serve_forever()
    def terminate(self):
        raise RuntimeError("raise SystemExit from terminate commands")
    def stop(self):
        # self.terminate()
        self.server.shutdown()
        self.terminate()
    def copy_report_to_home(self):
        report = ConfigManagerInstance.config["Report"]
        with open(report,"rb") as f:
            content = f.read()
        finally_report = join(self.home,"index.html")
        with open(finally_report,"wb") as f:
            f.write(content)
    def deploy_cgi(self):
        # report = ConfigManagerInstance.config["Report"]
        # reportDir = dirname(report)
        cgi_bin_path = join(os.getcwd(),"cgi-bin")
        createDir(cgi_bin_path)
        postOldFile = join(self.home,"cgi-bin","post.py")
        postNewFile = join(os.getcwd(),"cgi-bin","post.py")
        copyFile(postOldFile,postNewFile)



if __name__ == "__main__":
    S = server()
    S.start()