from library.library import singleton
from manager import EngineManagerInstance
from variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Security_002(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.describe = "Verify nbi3gc mf/proxy-1/proxy-2/proxy-3 security certificate path config is correct"

    def _checkpoint(self):
        get_value_from_configuration = EngineManagerInstance.get_keyword("get_value_from_configuration")
        item = "jacorb.security.keystore"
        self._nbi3gc_mf_keystore_path = get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy1_keystore_path = get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy2_keystore_path = get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES,item)
        self._nbi3gc_proxy3_keystore_path = get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES,item)
        self._nbi3gc_simulator_keystore_path = get_value_from_configuration(NBI3GC_SIMULATOR_PROPERTIES,item)
        self.logger.debug("nbi3gc-mf keystore path is:%s"%self._nbi3gc_mf_keystore_path)
        self.logger.debug("nbi3gc-proxy1 keystore path is:%s"%self._nbi3gc_proxy1_keystore_path)
        self.logger.debug("nbi3gc-proxy2 keystore path is:%s"%self._nbi3gc_proxy2_keystore_path)
        self.logger.debug("nbi3gc-proxy3 keystore path is:%s"%self._nbi3gc_proxy3_keystore_path)
        self.logger.debug("nbi3gc-simulator keystore path is:%s"%self._nbi3gc_simulator_keystore_path)
        if self._nbi3gc_mf_keystore_path == self._nbi3gc_proxy1_keystore_path == self._nbi3gc_proxy2_keystore_path == self._nbi3gc_proxy3_keystore_path:
            self.status = PASS
        else:
            self.status = FAIL









