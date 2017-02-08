from library.library import singleton
from manager import EngineManagerInstance
from variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Security_001(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.describe = "Item `jacorb.security.support_ssl` should be `on` in jacorb.properties"

    def _checkpoint(self):
        get_value_from_configuration = EngineManagerInstance.get_keyword("get_value_from_configuration")
        item = "jacorb.security.support_ssl"
        self._nbi3gc_mf_ssl_support = get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy1_ssl_support = get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy2_ssl_support = get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy3_ssl_support = get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES,item)
        self._nbi3gc_simulator_ssl_support = get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,item)
        self.logger.debug("nbi3gc-mf ssl support is:%s"%self._nbi3gc_mf_ssl_support)
        self.logger.debug("nbi3gc-proxy1 ssl support is:%s"%self._nbi3gc_proxy1_ssl_support)
        self.logger.debug("nbi3gc-proxy2 ssl support is:%s"%self._nbi3gc_proxy2_ssl_support)
        self.logger.debug("nbi3gc-proxy3 ssl support is:%s"%self._nbi3gc_proxy3_ssl_support)
        self.logger.debug("nbi3gc-simulator ssl support is:%s"%self._nbi3gc_simulator_ssl_support)
        if self._nbi3gc_mf_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ."%(NBI3GC_MF_JACORB_PROPERTIES,self._nbi3gc_mf_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("reset %s:jacorb.security.support_ssl current value is `on` ." % NBI3GC_MF_JACORB_PROPERTIES)
        if self._nbi3gc_proxy1_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ." %(NBI3GC_PROXY1_JACORB_PROPERTIES,self._nbi3gc_proxy1_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("reset %s:jacorb.security.support_ssl current value is `on` ."%NBI3GC_PROXY1_JACORB_PROPERTIES)
        if self._nbi3gc_proxy2_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ." %(NBI3GC_PROXY2_JACORB_PROPERTIES,self._nbi3gc_proxy2_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("reset %s:jacorb.security.support_ssl current value is `on` ." % NBI3GC_PROXY2_JACORB_PROPERTIES)

        if self._nbi3gc_proxy3_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ." %(NBI3GC_PROXY3_JACORB_PROPERTIES,self._nbi3gc_proxy3_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("reset %s:jacorb.security.support_ssl current value is `on` ." % NBI3GC_PROXY3_JACORB_PROPERTIES)
        if self._nbi3gc_simulator_ssl_support != "on":
            self.RCA.append("%s:jacorb.security.support_ssl current value is `%s`,Expect value is `on` ." %(NBI3GC_SIMULATOR_PROPERTIES,self._nbi3gc_simulator_ssl_support))
            self.IMPACT.append("3GPP Corba FM worked on inSecurity mode.")
            self.FIXSTEP.append("reset %s:jacorb.security.support_ssl current value is `on` ." % NBI3GC_SIMULATOR_PROPERTIES)
        if self._nbi3gc_simulator_ssl_support == self._nbi3gc_mf_ssl_support == self._nbi3gc_proxy1_ssl_support == self._nbi3gc_proxy2_ssl_support == self._nbi3gc_proxy3_ssl_support:
            self.status = PASS
        else:
            self.status = FAIL
            self.IMPACT.append("3GPP Corba FM maybe not work normally because Security mode is not matched")








