from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcCipherShouldBeValid(_BaseTestPoint):
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

        _allCipher =  _strongCipher + _weakCipher
        _strongCipher = set(_strongCipher)
        _weakCipher = set(_weakCipher)
        _allCipher = set(_allCipher)
        client_cipher_key = "jacorb.security.ssl.server.cipher_suites"
        server_cipher_key = "jacorb.security.ssl.client.cipher_suites"

        self._nbi3gc_mf_client_cipher = set(self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,client_cipher_key).split(","))
        self._nbi3gc_mf_server_cipher = set(self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,server_cipher_key).split(","))

        self._nbi3gc_proxy1_client_cipher = set(self.get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES,client_cipher_key).split(","))
        self._nbi3gc_proxy1_server_cipher = set(self.get_value_from_configuration(NBI3GC_PROXY1_JACORB_PROPERTIES, server_cipher_key).split(","))

        self._nbi3gc_proxy2_client_cipher = set(self.get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES,client_cipher_key).split(","))
        self._nbi3gc_proxy2_server_cipher = set(self.get_value_from_configuration(NBI3GC_PROXY2_JACORB_PROPERTIES, server_cipher_key).split(","))


        self._nbi3gc_proxy3_client_cipher= set(self.get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES,client_cipher_key).split(","))
        self._nbi3gc_proxy3_server_cipher = set(self.get_value_from_configuration(NBI3GC_PROXY3_JACORB_PROPERTIES, server_cipher_key).split(","))



        print "nbi3gc-mr client strong ciphers : %s"%",".join(self._nbi3gc_mf_client_cipher & _strongCipher)
        print "nbi3gc-mr client weak ciphers : %s" % ",".join(self._nbi3gc_mf_client_cipher & _weakCipher)
        print "nbi3gc-mr client invalid ciphers : %s" % ",".join(self._nbi3gc_mf_client_cipher.difference(_allCipher))

        print "nbi3gc-mr server strong ciphers : %s"%",".join(self._nbi3gc_mf_server_cipher & _strongCipher)
        print "nbi3gc-mr server weak ciphers : %s" % ",".join(self._nbi3gc_mf_server_cipher & _weakCipher)
        print "nbi3gc-mr server invalid ciphers : %s" % ",".join(self._nbi3gc_mf_server_cipher.difference(_allCipher))

        print "nbi3gc-proxy1 client strong ciphers : %s"%",".join(self._nbi3gc_proxy1_client_cipher & _strongCipher)
        print "nbi3gc-proxy1 client weak ciphers : %s" % ",".join(self._nbi3gc_proxy1_client_cipher & _weakCipher)
        print "nbi3gc-proxy1 client invalid ciphers : %s" % ",".join(self._nbi3gc_proxy1_client_cipher.difference(_allCipher))

        print "nbi3gc-proxy1 server strong ciphers : %s"%",".join(self._nbi3gc_proxy1_server_cipher & _strongCipher)
        print "nbi3gc-proxy1 server weak ciphers : %s" % ",".join(self._nbi3gc_proxy1_server_cipher & _weakCipher)
        print "nbi3gc-proxy1 server invalid ciphers : %s" % ",".join(self._nbi3gc_proxy1_server_cipher.difference(_allCipher))

        print "nbi3gc-proxy2 client strong ciphers : %s"%",".join(self._nbi3gc_proxy2_client_cipher & _strongCipher)
        print "nbi3gc-proxy2 client weak ciphers : %s" % ",".join(self._nbi3gc_proxy2_client_cipher & _weakCipher)
        print "nbi3gc-proxy2 client invalid ciphers : %s" % ",".join(self._nbi3gc_proxy2_client_cipher.difference(_allCipher))

        print "nbi3gc-proxy2 server strong ciphers : %s"%",".join(self._nbi3gc_proxy2_server_cipher & _strongCipher)
        print "nbi3gc-proxy2 server weak ciphers : %s" % ",".join(self._nbi3gc_proxy2_server_cipher & _weakCipher)
        print "nbi3gc-proxy2 server invalid ciphers : %s" % ",".join(self._nbi3gc_proxy2_server_cipher.difference(_allCipher))

        print "nbi3gc-proxy3 client strong ciphers : %s"%",".join(self._nbi3gc_proxy3_client_cipher & _strongCipher)
        print "nbi3gc-proxy3 client weak ciphers : %s" % ",".join(self._nbi3gc_proxy3_client_cipher & _weakCipher)
        print "nbi3gc-proxy3 client invalid ciphers : %s" % ",".join(self._nbi3gc_proxy3_client_cipher.difference(_allCipher))

        print "nbi3gc-proxy3 server strong ciphers : %s"%",".join(self._nbi3gc_proxy3_server_cipher & _strongCipher)
        print "nbi3gc-proxy3 server weak ciphers : %s" % ",".join(self._nbi3gc_proxy3_server_cipher & _weakCipher)
        print "nbi3gc-proxy3 server invalid ciphers : %s" % ",".join(self._nbi3gc_proxy3_server_cipher.difference(_allCipher))






        self.status = STATUS.PASS
        if not self._nbi3gc_mf_client_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-mf client cipher contain invalid cipher %s"%",".join(self._nbi3gc_mf_client_cipher.difference(_allCipher)))
        if not self._nbi3gc_mf_server_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-mf server cipher contain invalid cipher %s"%",".join(self._nbi3gc_mf_server_cipher.difference(_allCipher)))

        if not self._nbi3gc_proxy1_client_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy1 client cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy1_client_cipher.difference(_allCipher)))
        if not self._nbi3gc_proxy1_server_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy1 server cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy1_server_cipher.difference(_allCipher)))

        if not self._nbi3gc_proxy2_client_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy2 client cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy2_client_cipher.difference(_allCipher)))
        if not self._nbi3gc_proxy2_server_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy2 server cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy2_server_cipher.difference(_allCipher)))


        if not self._nbi3gc_proxy3_client_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy3 client cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy3_client_cipher.difference(_allCipher)))
        if not self._nbi3gc_proxy3_server_cipher.issubset(_allCipher):
            self.status = STATUS.FAIL
            self.RCA.append("nbi3gc-proxy3 server cipher contain invalid cipher %s"%",".join(self._nbi3gc_proxy3_server_cipher.difference(_allCipher)))


