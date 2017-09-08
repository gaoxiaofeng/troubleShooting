# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.template._BaseKeyword import _BaseKeyword
@singleton
class IRPAgentMgr(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._IRPAgentMgr_Path = "/opt/oss/NSN-nbi3gc/bin/nbi3gc_IRPAgentMgr.sh"
        self._proxy_deployed_status = {}
    def get_proxy_deploy_status(self,proxyid):
        if self._proxy_deployed_status == {}:
            self._list()
        if self._proxy_deployed_status.has_key(proxyid):
            return self._proxy_deployed_status[proxyid]
        else:
            return False
    def _list(self):
        command = "sh %s l"%self._IRPAgentMgr_Path
        stdout = self.execute_command(command)
        self._parse_list(stdout)

    def _parse_list(self,content):
        _lines = content.split("\n")
        for _line in _lines:
            if "IRPAgent-1" in _line:
                status  = True if "running" in _line else False
                self._proxy_deployed_status.update({PROXY.PROXY1:status})
            elif "IRPAgent-2" in _line:
                status  = True if "running" in _line else False
                self._proxy_deployed_status.update({PROXY.PROXY2:status})
            elif "IRPAgent-3" in _line:
                status  = True if "running" in _line else False
                self._proxy_deployed_status.update({PROXY.PROXY3:status})
            else:
                pass










