from troubleshooting.framework.modules.configuration import ConfigManagerInstance
from troubleshooting.framework.remote.client import client
from troubleshooting.framework.libraries.library import ExecuteCommond
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.log.internalLog import internalLog
import sys
import traceback
try:
    #import project config.variable
    from config.variable import *
except:
    print "WARN: failed to import config.variable"
class Recovery(object):
    def __init__(self):
        super(Recovery,self).__init__()
        self.remote = True if ConfigManagerInstance.config["Host"] else False
        self.host = ConfigManagerInstance.config["Host"]
        self.port = int(ConfigManagerInstance.config["Port"])
        self.user = ConfigManagerInstance.config["User"]
        self.password = ConfigManagerInstance.config["Password"]
        self.ssh = None
        self.local = None
        self.log = internalLog()
        self.internalLog = ""
    def _redirect(self):
        self._stdout = sys.stdout
        sys.stdout = self.log
    def _recover(self):
        if self._stdout:
            sys.stdout = self._stdout
    def run(self,*args):
        try:
            self._redirect()
            status = self.action(*args)
        except Exception,e:
            print traceback.format_exc()
            status = STATUS.FAIL
        finally:
            self._recover()
            self.internalLog = self.log.getContent()
        return  status,self.internalLog
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
    def execute_command(self,command):
        if self.remote:
            stdout = self._remote_execute_command(command)
            return stdout
        else:
            stdout = self._local_execute_command(command)
            return  stdout