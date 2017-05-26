from log.logger import logger
from variable.variable import *
from output.output import OutPutQueue
from library.library import parseRule
from manager import TestPointManager
from configuration import  ConfigManagerInstance
from manager import EngineManagerInstance
class _BaseTestPoint(object):
    def __init__(self):
        super(_BaseTestPoint,self).__init__()
        self.logger = logger()
        self.status = STATUS.NOTRUN
        self._ToPrint = True
        self._firstTestPoint = True
        self.RCA = []
        self.IMPACT = []
        self.FIXSTEP = []
        self.level = LEVEL.NOCRITICAL
        self.needRestartNbi3gcAfterFixed = False
        self._load_keyword()

    def _load_keyword(self):
        keywords = EngineManagerInstance.get_keyword()
        for instanceName in keywords:
            for keywordName in keywords[instanceName]:
                if  vars(self).has_key(keywordName):
                    pass
                else:
                    vars(self)[keywordName] = keywords[instanceName][keywordName]

    def get_keyword(self,keywordName):
        keyword = EngineManagerInstance.get_keyword(keywordName)
        return  keyword

    def _printf(self,message):
        if self._ToPrint:
            OutPutQueue.put(message)

    def _checkpoint(self):
        pass

    @property
    def passed(self):
        return self.status == STATUS.PASS


    def run(self,firstTestPoint=True):

        self._checkpoint()
        self.logger.info("TestPoint(%s) result is [%s]"%(self.__class__.__name__,self.status))
        if self.passed is False and self.needRestartNbi3gcAfterFixed:
            restartNbi3gcStep = """restart 3GPP Corba FM by below command:
\t\t\t#smanager.pl stop service nbi3gc
\t\t\t#smanager.pl start service nbi3gc"""
            self.FIXSTEP.append(restartNbi3gcStep)
        return self.passed,self.level,self.RCA,self.IMPACT,self.FIXSTEP,self.__doc__




