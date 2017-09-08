from troubleshooting.framework.remote.SSHLibrary import SSHLibrary
from troubleshooting.framework.libraries.library import singleton
@singleton
class client(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._connection_cache = {}
    def open_connection(self,host,port,user,password):
        if self._connection_cache.has_key(host):
            return self._connection_cache[host]
        else:
            ssh = SSHLibrary()
            ssh.open_connection(host=host,port=port,username=user,password=password)
            self._connection_cache.update({host:ssh})
            return ssh