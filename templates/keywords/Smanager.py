# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template._BaseKeyword import _BaseKeyword

@singleton
class Smanager(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._path = "/etc/init.d/"
        self._nbi3gc = "/etc/init.d/nbi3gc"
        self._nbi3gcom = "/etc/init.d/nbi3gcom"
        self._status_map = {}
    def _nbi3gc_status(self):
        command = "%s status"%self._nbi3gc
        stdout = self.execute_command(command)
        if "running" in stdout:
            self._status_map.update({"nbi3gc":True})
        else:
            self._status_map.update({"nbi3gc": False})
    def _nbi3gcom_status(self):
        command = "%s status"%self._nbi3gcom
        stdout = self.execute_command(command)
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




