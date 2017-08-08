from framework.library.library import ExecuteCommond,singleton
import  sys,os
from framework.output.Print import CONSOLE
import re

def Strip(c):
    return c.strip()

@singleton
class NamingService(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.jar_command = ExecuteCommond().jar_command
        self._GetIORFromNS_Path = "/opt/oss/NSN-nbi3gc/simulator/"
        self._GetIORFromNS_Jar = "GetIORFromNS.jar"
        self._irp_registed = {}
    def get_irp_from_ns(self,proxyid):
        if self._irp_registed == {}:
            self._list()
        if self._irp_registed.has_key(proxyid):
            return self._irp_registed[proxyid]
        else:
            return []
    def _list(self):

        stdout = self.jar_command(self._GetIORFromNS_Path,self._GetIORFromNS_Jar,"-l")
        self._parse_list(stdout)

    def _parse_list(self,content):
        proxyIor = {}
        pattern_proxy = re.compile(r"(^ {3}\S+\s)((^ {3}\t\S+\s)(^ {3}\t{2}\S+\s){1,}){1,}", re.M | re.S)
        pattern_irp = re.compile(r"(^ {3}\t{2}\S+\s)", re.M | re.S)
        for m in pattern_proxy.finditer(content):
            proxyId = m.group(1).strip().strip("/")
            proxyContent = m.group(0)

            irp = pattern_irp.findall(proxyContent)
            irp = map(Strip, irp)
            proxyIor.update({proxyId: irp})
        self._irp_registed = proxyIor








