from framework.library.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class SecurityShouldBeOn(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        # self.needRestartNbi3gcAfterFixed = True

    def _checkpoint(self):
        item = "jacorb.security.support_ssl"
        self._nbi3gc_mf_ssl_support = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,item)
        print "nbi3gc-mf ssl support is:%s"%self._nbi3gc_mf_ssl_support

        if self._nbi3gc_mf_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ."%(NBI3GC_MF_JACORB_PROPERTIES,self._nbi3gc_mf_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("manual reset %s:jacorb.security.support_ssl  value to `on` ." % NBI3GC_MF_JACORB_PROPERTIES)
            self.FIXSTEP.append("#smanager.pl stop service nbi3gc")
            self.FIXSTEP.append("#smanager.pl start service nbi3gc")
            self.status = STATUS.FAIL
        else:
            self.status = STATUS.PASS








