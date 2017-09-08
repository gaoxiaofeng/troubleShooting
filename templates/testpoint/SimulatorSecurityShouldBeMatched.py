from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.template._BaseTestPoint import _BaseTestPoint
@singleton
class SimulatorSecurityShouldBeMatched(_BaseTestPoint):
    """
    verify simulator and nbi3gc security mode are matched.
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self._simulator_ssl_mode = None
        self._nbi3gc_ssl_mode = None
    def _checkpoint(self):
        support_ssl = "jacorb.security.support_ssl"

        self._nbi3gc_mf_ssl_support = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,support_ssl)
        self._simulator_ssl_support = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,support_ssl)
        self._simulator_client_supported_options = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,"jacorb.security.ssl.client.supported_options")
        self._simulator_client_required_options = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,"jacorb.security.ssl.client.required_options")
        self._simulator_server_supported_options = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,"jacorb.security.ssl.server.supported_options")
        self._simulator_server_required_options = self.get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,"jacorb.security.ssl.server.required_options")

        if self._simulator_ssl_support == "off":
            self._simulator_ssl_mode = SECUREMOD.INSECURE
        else:
            if self._simulator_client_supported_options == "60" and \
            self._simulator_client_required_options == "0" and \
            self._simulator_server_supported_options == "60" and \
            self._simulator_server_required_options == "0":
                self._simulator_ssl_mode = SECUREMOD.COMPATIBLE
            else:
                self._simulator_ssl_mode = SECUREMOD.SECURE
        if self._nbi3gc_mf_ssl_support == "off":
            self._nbi3gc_ssl_mode = SECUREMOD.INSECURE
        else:
            self._nbi3gc_ssl_mode = SECUREMOD.SECURE




        print "nbi3gc-mf secure mode is:%s"%self._nbi3gc_ssl_mode
        print "nbi3gc-simulator secure mode is:%s"%self._simulator_ssl_mode
        if self._simulator_ssl_mode == SECUREMOD.COMPATIBLE or self._simulator_ssl_mode == self._nbi3gc_ssl_mode :
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("Simulators could not operate nbi3gc service.")
            RCA = """The secure mode is different between simualtors and nbi3gc service:
\t\t\tsimulators secure mode is `%s`.
\t\t\tnbi3gc service secure mode is `%s`."""%(self._simulator_ssl_mode,self._nbi3gc_ssl_mode)
            self.RCA.append(RCA)

            fixStep = []

            fixStep.append("manual reset %s:jacorb.security.support_ssl to `%s`." % (NBI3GC_SIMULATOR_PROPERTIES,self._nbi3gc_mf_ssl_support))
            fixStepStr = "\n\t\t\t".join(fixStep)
            self.FIXSTEP.append(fixStepStr)



