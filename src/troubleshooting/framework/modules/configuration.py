# -*- coding: utf-8 -*-
import ConfigParser
import os,sys
#@singleton
class ConfigManager(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.__config = {}
    @property
    def config(self):
        return  self.__config
    @config.setter
    def config(self,Map):
        # for key in Map:
        #     self.__config[key] = Map[key]
        self.__config.update(Map)



ConfigManagerInstance = ConfigManager()

CP = ConfigParser.SafeConfigParser()
configFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"conf","init.conf")
with open(configFilePath,"r") as f:
    CP.readfp(f)
ConfigManagerInstance.config["report_total_width"] =  CP.getint("report","total_width")
ConfigManagerInstance.config["report_table_width"] =  CP.getint("report","table_width")