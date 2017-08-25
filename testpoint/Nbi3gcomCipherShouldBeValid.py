from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcomCipherShouldBeValid(_BaseTestPoint):
    """
    verify nbi3gc secure ciphers should be valid.
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.CRITICAL

    def _checkpoint(self):
        _strongCipher = ["TLS_DHE_RSA_WITH_AES_128_GCM_SHA256","TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",\
                              "TLS_RSA_WITH_AES_128_GCM_SHA256","TLS_RSA_WITH_AES_256_GCM_SHA384"]

        _weakCipher = ["TLS_DHE_RSA_WITH_AES_256_CBC_SHA256","TLS_DHE_RSA_WITH_AES_256_CBC_SHA",\
                           "TLS_RSA_WITH_AES_256_CBC_SHA256","TLS_RSA_WITH_AES_256_CBC_SHA",\
                            "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256","TLS_DHE_RSA_WITH_AES_128_CBC_SHA",\
                            "TLS_RSA_WITH_AES_128_CBC_SHA256","TLS_RSA_WITH_AES_128_CBC_SHA"]
        __weakCipher = ["SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA","SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA",\
                        "SSL_RSA_WITH_3DES_EDE_CBC_SHA","TLS_DHE_DSS_WITH_AES_128_CBC_SHA"]
        _weakCipher += __weakCipher
        _allCipher =  _strongCipher + _weakCipher
        _strongCipher = set(_strongCipher)
        _weakCipher = set(_weakCipher)
        _allCipher = set(_allCipher)
        client_cipher_key = "jacorb.security.ssl.server.cipher_suites"
        server_cipher_key = "jacorb.security.ssl.client.cipher_suites"

        self._nbi3gcom_mf_client_cipher = set(self.get_value_from_configuration(NBI3GCOM_PROPERTIES,client_cipher_key).split(","))
        self._nbi3gcom_mf_server_cipher = set(self.get_value_from_configuration(NBI3GCOM_PROPERTIES,server_cipher_key).split(","))



        print "nbi3gcom client strong ciphers : %s"%",".join(self._nbi3gcom_mf_client_cipher & _strongCipher)
        print "nbi3gcom client weak ciphers : %s" % ",".join(self._nbi3gcom_mf_client_cipher & _weakCipher)
        print "nbi3gcom client invalid ciphers : %s" % ",".join(self._nbi3gcom_mf_client_cipher.difference(_allCipher))

        print "nbi3gcom server strong ciphers : %s"%",".join(self._nbi3gcom_mf_server_cipher & _strongCipher)
        print "nbi3gcom server weak ciphers : %s" % ",".join(self._nbi3gcom_mf_server_cipher & _weakCipher)
        print "nbi3gcom server invalid ciphers : %s" % ",".join(self._nbi3gcom_mf_server_cipher.difference(_allCipher))






        self.status = STATUS.PASS
        if not self._nbi3gcom_mf_client_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gcom client cipher contain invalid cipher %s"%",".join(self._nbi3gcom_mf_client_cipher.difference(_allCipher)))
        if not self._nbi3gcom_mf_server_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gcom server cipher contain invalid cipher %s"%",".join(self._nbi3gcom_mf_server_cipher.difference(_allCipher)))

