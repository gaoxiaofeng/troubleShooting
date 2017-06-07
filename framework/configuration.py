# from  library.library import  singleton
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
        for key in Map:
            self.__config[key] = Map[key]



ConfigManagerInstance = ConfigManager()
