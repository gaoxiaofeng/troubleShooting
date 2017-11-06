from troubleshooting.framework.modules.configuration import ConfigManagerInstance
from troubleshooting.framework.remote.client import client
from troubleshooting.framework.libraries.library import ExecuteCommond
try:
    #import project config.variable
    from config.variable import *
except:
    print "WARN: failed to import config.variable"
class Keyword(object):
    def __init__(self):
        super(Keyword,self).__init__()
        self.remote = True if ConfigManagerInstance.config["Host"] else False
        self.host = ConfigManagerInstance.config["Host"]
        self.port = int(ConfigManagerInstance.config["Port"])
        self.user = ConfigManagerInstance.config["User"]
        self.password = ConfigManagerInstance.config["Password"]
        self.ssh = None
        self.local = None
    def _open_connection(self):
        self.ssh = client().open_connection(host=self.host,port=self.port,user=self.user,password=self.password)
    def _remote_execute_command(self,command,checkerr = False):
        if self.ssh is None:
            self._open_connection()
        stdout = self.ssh._execute_command(command,checkerr=checkerr)
        return stdout

    def _local_execute_command(self,command,checkerr = True):
        if self.local is None:
            self.local =  ExecuteCommond()
        stdout = self.local.shell_command(command,checkerr=checkerr)
        return stdout
    def execute_command(self,command,checkerr = False):
        if self.remote:
            stdout = self._remote_execute_command(command,checkerr=checkerr)
            return stdout
        else:
            stdout = self._local_execute_command(command)
            return  stdout

    def download(self,remoteFile,localFile):
        self.ssh.get(remoteFile,localFile)
