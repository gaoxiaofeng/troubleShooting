from framework.library.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class SecurityShouldBeMatched(_BaseTestPoint):
    """
    verify nbi3gc and nbi3gcom security mode are matched.
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL
        self.needRestartNbi3gcAfterFixed = True

    def _checkpoint(self):
        item = "jacorb.security.support_ssl"
        self._nbi3gc_mf_ssl_support = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy1_ssl_support = self.get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy2_ssl_support = self.get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy3_ssl_support = self.get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES,item)
        self._nbi3gcom_ssl_support = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,item)
        # self._nbi3gc_simulator_ssl_support = get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,item)
        self.logger.debug("nbi3gc-mf ssl support is:%s"%self._nbi3gc_mf_ssl_support)
        self.logger.debug("nbi3gc-proxy1 ssl support is:%s"%self._nbi3gc_proxy1_ssl_support)
        self.logger.debug("nbi3gc-proxy2 ssl support is:%s"%self._nbi3gc_proxy2_ssl_support)
        self.logger.debug("nbi3gc-proxy3 ssl support is:%s"%self._nbi3gc_proxy3_ssl_support)
        self.logger.debug("nbi3gcom ssl support is:%s"%self._nbi3gcom_ssl_support)
        # self.logger.debug("nbi3gc-simulator ssl support is:%s"%self._nbi3gc_simulator_ssl_support)
        if  self._nbi3gc_mf_ssl_support == self._nbi3gc_proxy1_ssl_support == self._nbi3gc_proxy2_ssl_support == self._nbi3gc_proxy3_ssl_support == self._nbi3gcom_ssl_support:
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("3GPP Corba FM Security mode is not working normally.")
            # self.IMPACT.append("Both Operation and Notification Forwarding are not appropriate working.")
            RCA = """Items `jacorb.security.support_ssl` are not matched as below:
\t\t\t%s : jacorb.security.support_ssl current value is `%s`.
\t\t\t%s : jacorb.security.support_ssl current value is `%s`.
\t\t\t%s : jacorb.security.support_ssl current value is `%s`.
\t\t\t%s : jacorb.security.support_ssl current value is `%s`.
\t\t\t%s : jacorb.security.support_ssl current value is `%s`"""%(NBI3GC_MF_JACORB_PROPERTIES,self._nbi3gc_mf_ssl_support,NBI3GC_PROXY1_JACORB_PROPERTIES, self._nbi3gc_proxy1_ssl_support,NBI3GC_PROXY2_JACORB_PROPERTIES, self._nbi3gc_proxy2_ssl_support,
                 NBI3GC_PROXY3_JACORB_PROPERTIES, self._nbi3gc_proxy3_ssl_support,NBI3GCOM_PROPERTIES,self._nbi3gcom_ssl_support)
            self.RCA.append(RCA)

            fixStep = []
            fixStep.append("if you want 3GPP Corba FM working on Security mode:")
            if self._nbi3gc_mf_ssl_support != "on":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `on`."% NBI3GC_MF_JACORB_PROPERTIES)
            if self._nbi3gc_proxy1_ssl_support != "on":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `on`." % NBI3GC_PROXY1_JACORB_PROPERTIES)
            if self._nbi3gc_proxy2_ssl_support != "on":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `on`." % NBI3GC_PROXY2_JACORB_PROPERTIES)
            if self._nbi3gc_proxy3_ssl_support != "on":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `on`." % NBI3GC_PROXY3_JACORB_PROPERTIES)
            if self._nbi3gcom_ssl_support != "on":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `on`." % NBI3GCOM_PROPERTIES )

            fixStepStr = "\n\t\t\t".join(fixStep)
            self.FIXSTEP.append(fixStepStr)
            fixStep = []
            fixStep.append("if you want 3GPP Corba FM working on InSecurity mode:")
            if self._nbi3gc_mf_ssl_support != "off":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `off`."% NBI3GC_MF_JACORB_PROPERTIES)
            if self._nbi3gc_proxy1_ssl_support != "off":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `off`." % NBI3GC_PROXY1_JACORB_PROPERTIES)
            if self._nbi3gc_proxy2_ssl_support != "off":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `off`." % NBI3GC_PROXY2_JACORB_PROPERTIES)
            if self._nbi3gc_proxy3_ssl_support != "off":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `off`." % NBI3GC_PROXY3_JACORB_PROPERTIES)
            if self._nbi3gcom_ssl_support != "off":
                fixStep.append("manual reset %s:jacorb.security.support_ssl to `off`." % NBI3GCOM_PROPERTIES )
            fixStepStr = "\n\t\t\t".join(fixStep)
            self.FIXSTEP.append(fixStepStr)



