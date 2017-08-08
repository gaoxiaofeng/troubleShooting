from framework.library.library import singleton,conversion
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcServiceCheck(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL

    def _checkpoint(self):
        if self.get_nbi3gc_service_status():
            smx_status,smx_status_map = self.get_nbi3gc_smx_status()
            if smx_status:
                print "nbi3gc service was started"
                self.status = STATUS.PASS
            else:
                print "nbi3gc service was starting"
                for key in smx_status_map:
                    if smx_status_map[key] != "Started":
                        print "nbi3gc %s stauts --> %s"%(key,smx_status_map[key])
                self.status = STATUS.FAIL
                self.IMPACT.append("nbi3gc was starting.")
                self.RCA.append("nbi3gc was starting.")
                self.FIXSTEP.append("wait for nbi3gc started.")
        else:
            print "nbi3gc service was not started"
            self.status = STATUS.FAIL
            self.IMPACT.append("nbi3gc was not started.")
            self.RCA.append("nbi3gc was not started.")
            self.FIXSTEP.append("#smanager.pl start service nbi3gc")