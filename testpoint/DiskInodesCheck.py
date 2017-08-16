from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class DiskInodesCheck(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()

    def _checkpoint(self):
        diskInodes = self.get_disk_usage_inodes()
        for key in diskInodes:
            if diskInodes[key] == "100":
                self.status = STATUS.FAIL
                self.IMPACT.append("no enough disk inodes in nbi3gc node")
                self.RCA.append("%s is full"%key)
                self.FIXSTEP.append("clean for %s"%key)
            else:
                print "%s inodes usage %s%%"%(key,diskInodes[key])

        if self.status != STATUS.FAIL:
            self.status = STATUS.PASS
