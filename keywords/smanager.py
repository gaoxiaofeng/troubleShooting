from framework.library.library import ExecuteCommond,singleton
import  sys,os
from framework.output.Print import CONSOLE
import re

@singleton
class Smanager(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.shell_script = ExecuteCommond().shell_script
        self._path = "/etc/init.d/"
        self._nbi3gc = "nbi3gc"
        self._nbi3gcom = "nbi3gcom"
        self._status_map = {}
    def _nbi3gc_status(self):

        stdout = self.shell_script(self._path,self._nbi3gc,"status")
        if "running" in stdout:
            self._status_map.update({"nbi3gc":True})
        else:
            self._status_map.update({"nbi3gc": False})
    def _nbi3gcom_status(self):
        stdout = self.shell_script(self._path,self._nbi3gcom,"status")
        if "running" in stdout:
            self._status_map.update({"nbi3gcom":True})
        else:
            self._status_map.update({"nbi3gcom": False})
    def _status(self):
        if self._status_map == {}:
            self._nbi3gc_status()
            self._nbi3gcom_status()
    def get_nbi3gc_service_status(self):
        self._status()
        if self._status_map.has_key("nbi3gc"):
            return self._status_map["nbi3gc"]
        else:
            raise Exception("fail to get nbi3gc service status.")

    def get_nbi3gcom_service_status(self):
        self._status()
        if self._status_map.has_key("nbi3gcom"):
            return self._status_map["nbi3gcom"]
        else:
            raise Exception("fail to get nbi3gcom service status.")




