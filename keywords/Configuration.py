# -*- coding: utf-8 -*-
import sys,os
from framework.libraries.library import singleton
from framework.log.logger import logger
from keywords._BaseKeyword import _BaseKeyword
@singleton
class Configuration(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._cache = {}
        self.logger = logger()
    def _get_config_content(self,configuration):
        command = "cat %s|grep -v '#'"%configuration
        stdout = self.execute_command(command)
        if not stdout:
            print "execute command: %s  , return: %s"%(command,stdout)
            return ""
        lines = []
        _lines = stdout.split("\n")
        for line in _lines:
            if "#" not in line:
                lines.append(line)
        result = "\n".join(lines)
        return result
    def _convert_to_map(self,content):
        config_map = {}
        for line in content.split("\n"):
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
                #self._cache[configuration] = config_map
                #dont cache for Reload configuration
            return config_map

    def get_value_from_configuration(self,configuration,item):
        config_map = self._get_configuration(configuration)
        if config_map.has_key(item):
            return config_map[item]
        else:
            print "configuration(%s) has not item(%s)!"%(configuration,item,)
            return ""



if __name__ == "__main__":
    obj = Configuration()
    print obj.get_value_from_configuration("/opt/oss/NSN-nbi3gc/smx/mf-conf/nbi-3gpp-corba.properties","com.nsn.oss.nbi.epirp.systemDn")
