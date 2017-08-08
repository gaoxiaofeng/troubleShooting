from framework.library.library import singleton,conversion
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcomServiceCheck(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL

    def _checkpoint(self):
        if self.get_nbi3gcom_service_status():
            print "nbi3gcom service was started"
            self.status = STATUS.PASS
        else:
            print "nbi3gcom service was not started"
            self.status = STATUS.FAIL
            self.IMPACT.append("nbi3gcom is not running.")
            self.RCA.append("nbi3gcom process is not running")
            self.FIXSTEP.append("#smanager.pl start service nbi3gcom")