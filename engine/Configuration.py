import sys,os
from library.library import ExecuteCommond,singleton
from log.logger import logger
@singleton
class Configuration(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._command = ExecuteCommond().shell_command
        self._cache = {}
        self.logger = logger()
    def _get_config_content(self,configuration):
        command = "cat %s |grep -v '#'"%configuration
        result = self._command(command)
        return result
    def _convert_to_map(self,content):
        config_map = {}
        for line in content.split(os.linesep):
            if "=" in line :
                equalMark = line.index("=")
                key = line[:equalMark].strip()
                value = line[equalMark+1:].strip()
                config_map[key] = value
        return config_map
    def _get_configuration(self,configuration):
        if self._cache.has_key(configuration):
            return self._cache[configuration]
        else:
            content = self._get_config_content(configuration)
            config_map = {}
            if content:
                config_map = self._convert_to_map(content)
                self._cache[configuration] = config_map
            return config_map

    def get_value_from_configuration(self,configuration,item):
        config_map = self._get_configuration(configuration)
        if config_map.has_key(item):
            return config_map[item]
        else:
            self.logger.error("get config(%s) item(%s) failed!configuration content is %s"%(configuration,item,config_map))
            return None



if __name__ == "__main__":
    obj = Configuration()
    print obj.get_value_from_configuration("/opt/oss/NSN-nbi3gc/smx/mf-conf/nbi-3gpp-corba.properties","com.nsn.oss.nbi.epirp.systemDn")
