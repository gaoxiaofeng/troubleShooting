from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template.TestPoint import *
@singleton
class DiskSizeCheck(TestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()

    def _checkpoint(self):
        diskSize = self.get_disk_usage_size()
        if not diskSize:
            #disSize = {}
            self.status = STATUS.FAIL
        for key in diskSize:
            if diskSize[key] == "100":
                self.status = STATUS.FAIL
                self.IMPACT.append("no enough disk space in this node")
                self.RCA.append("%s is full"%key)
                self.FIXSTEP.append("clean for %s"%key)
            else:
                print "%s size usage %s%%"%(key,diskSize[key])

        if self.status != STATUS.FAIL:
            self.status = STATUS.PASS
