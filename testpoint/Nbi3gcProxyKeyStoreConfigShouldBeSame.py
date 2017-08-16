from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcProxyKeyStoreConfigShouldBeSame(_BaseTestPoint):
    """
    check nbi3gc and nbi3gcom keystore
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL
        # self.needRestartNbi3gcAfterFixed = True

    def _checkpoint(self):
        keystorePathItem = "jacorb.security.keystore"
        self._nbi3gc_mf_keystore_path = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,keystorePathItem)
        self._nbi3gc_proxy1_keystore_path = self.get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES,keystorePathItem)
        self._nbi3gc_proxy2_keystore_path = self.get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES,keystorePathItem)
        self._nbi3gc_proxy3_keystore_path = self.get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES,keystorePathItem)
        if self._nbi3gc_mf_keystore_path == self._nbi3gc_proxy1_keystore_path == self._nbi3gc_proxy2_keystore_path \
            == self._nbi3gc_proxy3_keystore_path :
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("3GPP Corba FM Security mode is not working normally.")
            RCA = """Items `jacorb.security.keystore` are not matched as below:
            \t\t\t%s : jacorb.security.keystore current value is `%s`.
            \t\t\t%s : jacorb.security.keystore current value is `%s`.
            \t\t\t%s : jacorb.security.keystore current value is `%s`.
            \t\t\t%s : jacorb.security.keystore current value is `%s`.""" % (NBI3GC_MF_JACORB_PROPERTIES,self._nbi3gc_mf_keystore_path, \
                                                                            NBI3GC_PROXY1_JACORB_PROPERTIES,self._nbi3gc_proxy1_keystore_path, \
                                                                            NBI3GC_PROXY2_JACORB_PROPERTIES,self._nbi3gc_proxy3_keystore_path, \
                                                                            NBI3GC_PROXY3_JACORB_PROPERTIES,self._nbi3gc_proxy3_keystore_path)
            self.RCA.append(RCA)
            self.FIXSTEP.append("please reset the jacorb.security.keystore in relevant configuration.")
            self.FIXSTEP.append("#smanager.pl stop service nbi3gc")
            self.FIXSTEP.append("#smanager.pl start service nbi3gc")
