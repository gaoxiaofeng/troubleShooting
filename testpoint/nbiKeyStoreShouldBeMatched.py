from framework.library.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class nbiKeyStoreShouldBeMatched(_BaseTestPoint):
    """
    check nbi3gc and nbi3gcom keystore
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL
        self.needRestartNbi3gcAfterFixed = True

    def _checkpoint(self):
        keystorePathItem = "jacorb.security.keystore"
        keystorePasswdItem = "jacorb.security.keystore_password"
        self._nbi3gc_keystore_path = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,keystorePathItem)
        self._nbi3gcom_keystore_path = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,keystorePathItem)
        self._nbi3gc_keystore_passwd = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,keystorePasswdItem)
        self._nbi3gcom_keystore_passwd = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,keystorePasswdItem)
        print self.get_cert_from_keystore(self._nbi3gc_keystore_path,self._nbi3gc_keystore_passwd)