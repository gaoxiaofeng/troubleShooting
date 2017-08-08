from framework.library.library import ExecuteCommond,singleton
# import  sys,os
# from framework.output.Print import CONSOLE
import re

@singleton
class Smx(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.shell_script = ExecuteCommond().shell_script
        self._path = "/opt/oss/NSN-nbi3gc/bin/"
        self._smx = "smx-clt"
        self._status_map = {}
        self._status = None
    def _nbi3gc_smx_status(self):

        stdout = self.shell_script(self._path,self._smx,"status","1")
        pattern = re.compile(r"(^\S+) +(\S+) +(\S+ *\S*)\s", re.M | re.S)

        for m in pattern.finditer(stdout):
            if "IRP" in m.group(1) or "NBI-COMMON" in m.group(1):
                key = ":".join( [m.group(1), m.group(2)] )
                value =  m.group(3)
                self._status_map.update({key:value})


        pattern = re.compile(r"(\d+)%",re.M|re.S)
        match =  pattern.search(stdout)
        if match:
            status = match.group(1)
            if status == "100":
                self._status = True
            else:
                self._status = False

    def get_nbi3gc_smx_status(self):
        if self._status_map == {}:
            self._nbi3gc_smx_status()
        return  self._status,self._status_map


if __name__ == "__main__":
    smx = Smx()
    smx.test()



