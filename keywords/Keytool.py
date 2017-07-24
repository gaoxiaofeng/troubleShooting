from framework.library.library import ExecuteCommond,singleton
import  sys,os
@singleton
class Keytool(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.execute_command = ExecuteCommond().shell_command
    def get_cert_from_keystore(self,keystore,passwd):
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
        for content in __list:
            if "trustedCertEntry" in content:
                certs_map.update(self._parse_cert(content))
        return  certs_map


    def _parse_cert(self,content):
        cert_map = {}
        for line in content.split(os.linesep):
            if "Alias name" in line:
                alias = line[line.index(":")+1:].strip()
            if "MD5" in line:
                md5 = line[line.index(":")+1:].strip()
        cert_map[alias] = md5
        return  cert_map





