# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template._BaseKeyword import _BaseKeyword
import  sys,os
@singleton
class Keytool(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
    def get_cert_and_key_from_keystore(self,keystore,passwd):
        return  self._keytool_list(keystore,passwd)
    def _keytool_list(self,keystore,passwd):
        command = "keytool -v -list -keystore %s -storepass %s" % (keystore, passwd)
        stdout = self.execute_command(command)
        _split = """
*******************************************
*******************************************
        """.strip()
        _list = stdout.split(_split)
        __list = []
        for cert_key in _list:
            if "Alias name" in cert_key:
                __list.append(cert_key)
        certs_map = {}
        key_map = {}
        for content in __list:
            if "trustedCertEntry" in content:
                certs_map.update(self._parse_cert(content))
            if "PrivateKeyEntry" in content:
                key_map.update(self._parse_cert(content))
        print "cert:",certs_map
        print "key:",key_map
        return  certs_map,key_map


    def _parse_cert(self,content):
        cert_map = {}
        for line in content.split("\n"):
            if "Alias name" in line:
                alias = line[line.index(":")+1:].strip()
            if "MD5" in line:
                md5 = line[line.index(":")+1:].strip()
        cert_map[alias] = md5
        return  cert_map






