# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.log.logger import logger
class EngineException(Exception):
    pass



@singleton
class Engine(object):
    '''
    manager of Simulator and Tool
    '''
    _registry = {}
    def __init__(self):
        super(self.__class__,self).__init__()
        self.logger = logger()
    def __str__(self):
        return "Engine dict:%s"%self.__dict__
    __repr__ = __str__

    def register(self,instant):
        """
        register the class.
        """
        if not isinstance(instant,(type,)):
            raise EngineException("Engine.register: args must be a class.")

        self._registry[instant.__name__] = instant()
        self.logger.info("Engine.register:add instant %s"%instant.__name__)

    def get_all_instants(self):
        return self._registry
    def get_instant(self,name):
        if self._registry.has_key(name):
            return self._registry[name]
        else:
            raise EngineException("Engine.register: %s was not found in registed list"%name)







