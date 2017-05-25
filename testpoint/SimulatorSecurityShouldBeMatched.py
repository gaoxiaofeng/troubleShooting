from library.library import singleton
from manager import EngineManagerInstance
from variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class SimulatorSecurityShouldBeMatched(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        # self.describe = "Item `jacorb.security.support_ssl` consistency should be guaranteed in nbi3gc-mf ,simulator configuration."
        self.level = NOCRITICAL
        self.needRestartNbi3gcAfterFixed = False

    def _checkpoint(self):
        item = "jacorb.security.support_ssl"
        self._nbi3gc_mf_ssl_support = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,item)
        self._nbi3gc_simulator_ssl_support = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,item)
        self.logger.debug("nbi3gc-mf ssl support is:%s"%self._nbi3gc_mf_ssl_support)
        self.logger.debug("nbi3gc-simulator ssl support is:%s"%self._nbi3gc_simulator_ssl_support)
        if self._nbi3gc_simulator_ssl_support == self._nbi3gc_mf_ssl_support :
            self.status = PASS
        else:
            self.status = FAIL
            self.IMPACT.append("Simulators are not working normally which are under /opt/oss/NSN-nbi3gc/simulator folder.")
            RCA = """Items `jacorb.security.support_ssl` are not matched as below:
\t\t\t%s : jacorb.security.support_ssl current value is `%s`.
\t\t\t%s : jacorb.security.support_ssl current value is `%s`."""%(NBI3GC_MF_JACORB_PROPERTIES,self._nbi3gc_mf_ssl_support,NBI3GC_SIMULATOR_PROPERTIES, self._nbi3gc_simulator_ssl_support )
            self.RCA.append(RCA)

            fixStep = []

            fixStep.append("manual reset %s:jacorb.security.support_ssl to `%s`." % (NBI3GC_SIMULATOR_PROPERTIES,self._nbi3gc_mf_ssl_support))
            fixStepStr = "\n\t\t\t".join(fixStep)
            self.FIXSTEP.append(fixStepStr)



