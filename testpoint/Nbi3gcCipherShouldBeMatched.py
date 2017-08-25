from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcCipherShouldBeMatched(_BaseTestPoint):
    """
    verify nbi3gc secure ciphers are matched.
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.NOCRITICAL

    def _checkpoint(self):
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

        # print "nbi3gc-mf client cipher is:%s"%",".join(self._nbi3gc_mf_client_cipher)
        # print "nbi3gc-mf server cipher is:%s" % ",".join(self._nbi3gc_mf_server_cipher)
        #
        # print "nbi3gc-proxy1 client cipher is:%s"%",".join(self._nbi3gc_proxy1_client_cipher)
        # print "nbi3gc-proxy1 server cipher is:%s" % ",".join(self._nbi3gc_proxy1_server_cipher)
        #
        # print "nbi3gc-proxy2 client cipher is:%s"%",".join(self._nbi3gc_proxy2_client_cipher)
        # print "nbi3gc-proxy2 server cipher is:%s" % ",".join(self._nbi3gc_proxy2_server_cipher)
        #
        # print "nbi3gc-proxy3 client cipher is:%s"%",".join(self._nbi3gc_proxy3_client_cipher)
        # print "nbi3gc-proxy3 server cipher is:%s" % ",".join(self._nbi3gc_proxy3_server_cipher)


        if  (self._nbi3gc_mf_client_cipher == self._nbi3gc_proxy1_client_cipher == self._nbi3gc_proxy2_client_cipher == self._nbi3gc_proxy3_client_cipher) and \
                (self._nbi3gc_mf_server_cipher == self._nbi3gc_proxy1_server_cipher == self._nbi3gc_proxy2_server_cipher == self._nbi3gc_proxy3_server_cipher):
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("3GPP Corba FM Security mode maybe not working normally.")
            _client_cipher_diff = (self._nbi3gc_mf_client_cipher & self._nbi3gc_proxy1_client_cipher & self._nbi3gc_proxy2_client_cipher & self._nbi3gc_proxy3_client_cipher) ^ \
                                  (self._nbi3gc_mf_client_cipher | self._nbi3gc_proxy1_client_cipher | self._nbi3gc_proxy2_client_cipher | self._nbi3gc_proxy3_client_cipher)
            _server_cipher_diff = (self._nbi3gc_mf_server_cipher & self._nbi3gc_proxy1_server_cipher & self._nbi3gc_proxy2_server_cipher & self._nbi3gc_proxy3_server_cipher) ^\
                                  (self._nbi3gc_mf_server_cipher | self._nbi3gc_proxy1_server_cipher | self._nbi3gc_proxy2_server_cipher | self._nbi3gc_proxy3_server_cipher)

            if _client_cipher_diff:
                self.RCA.append("secure client Cipher list %s is not matched for nbi3gc mf/proxy-x"%list(_client_cipher_diff) )
            if _server_cipher_diff:
                self.RCA.append("secure server Cipher list %s is not matched for nbi3gc mf/proxy-x" % list(_server_cipher_diff))

            self.FIXSTEP.append("reset secure cipher for mf/proxy-x ")
