from framework.library.library import singleton,dict_value_contain_content
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
        # self.needRestartNbi3gcAfterFixed = True
        # self.needRestartNbi3gcomAfterFixed = True
        self.nbi3gc_cert = "/d/oss/global/certificate/nbi3gc/nbi3gc.crt"
        self.nbi3gcom_cert = "/d/oss/global/certificate/nbi3gcom/nbi3gcom.crt"
    def _checkpoint(self):
        keystorePathItem = "jacorb.security.keystore"
        keystorePasswdItem = "jacorb.security.keystore_password"
        self._nbi3gc_keystore_path = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,keystorePathItem)
        self._nbi3gcom_keystore_path = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,keystorePathItem)
        self._nbi3gc_keystore_passwd = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,keystorePasswdItem)
        self._nbi3gcom_keystore_passwd = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,keystorePasswdItem)
        nbi3gc_keystore_cert_dict,nbi3gc_keystore_key_dict = self.get_cert_and_key_from_keystore(self._nbi3gc_keystore_path,self._nbi3gc_keystore_passwd)
        nbi3gc_private_key_alias = nbi3gc_keystore_key_dict.keys()[0]
        nbi3gc_private_key_value =  nbi3gc_keystore_key_dict[nbi3gc_private_key_alias]
        nbi3gc_cert_sha1 = nbi3gc_private_key_value
        print "nbi3gc keystore contain certificate : %s"%nbi3gc_keystore_cert_dict
        print "nbi3gc keystore contain private key:%s"%nbi3gc_keystore_key_dict
        nbi3gcom_keystore_cert_dict,nbi3gcom_keystore_key_dict = self.get_cert_and_key_from_keystore(self._nbi3gcom_keystore_path,self._nbi3gcom_keystore_passwd)
        print "nbi3gcom keystore contain certificate : %s"%nbi3gcom_keystore_cert_dict
        print "nbi3gcom keystore contain private key:%s"%nbi3gcom_keystore_key_dict
        nbi3gcom_private_key_alias = nbi3gcom_keystore_key_dict.keys()[0]
        nbi3gcom_private_key_value = nbi3gcom_keystore_key_dict[nbi3gcom_private_key_alias]
        nbi3gcom_cert_sha1 = nbi3gcom_private_key_value


        if dict_value_contain_content(nbi3gc_keystore_cert_dict,nbi3gcom_cert_sha1):
            pass
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("nbi3gc could not work normally.")
            self.RCA.append("nbi3gc keystore has not contain nbi3gcom certificate")
            self.FIXSTEP.append("keytool -import -alias %s -keystore %s -file %s -storepass %s"%(nbi3gcom_private_key_alias,self._nbi3gc_keystore_path,self.nbi3gcom_cert,self._nbi3gc_keystore_passwd))

        if dict_value_contain_content(nbi3gcom_keystore_cert_dict,nbi3gc_cert_sha1):
            pass
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("nbi3gc could not work normally.")
            self.RCA.append("nbi3gcom keystore has not contain nbi3gc certificate")
            self.FIXSTEP.append("keytool -import -alias %s -keystore %s -file %s -storepass %s"%(nbi3gc_private_key_alias,self._nbi3gcom_keystore_path,self.nbi3gc_cert,self._nbi3gcom_keystore_passwd))
        if self.status is not STATUS.FAIL:
            self.status = STATUS.PASS

        if self.FIXSTEP:
            self.FIXSTEP.append("#smanager.pl stop service nbi3gcom")
            self.FIXSTEP.append("#smanager.pl stop service nbi3gc")
            self.FIXSTEP.append("#smanager.pl start service nbi3gcom")
            self.FIXSTEP.append("#smanager.pl start service nbi3gc")