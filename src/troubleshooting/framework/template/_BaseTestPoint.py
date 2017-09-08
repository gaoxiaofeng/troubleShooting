# -*- coding: utf-8 -*-
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.output.output import OutPutQueue
from troubleshooting.framework.libraries.library import parseRule,RemoveDuplicates
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.log.internalLog import internalLog
import sys
class _BaseTestPoint(object):
    def __init__(self):
        super(_BaseTestPoint,self).__init__()
        self.keywordManager = ManagerFactory().getManager(LAYER.KeyWords)
        self.logger = logger()
        self.status = STATUS.NOTRUN
        self._ToPrint = True
        self._firstTestPoint = True
        self.RCA = []
        self.IMPACT = []
        self.FIXSTEP = []
        self.level = LEVEL.NOCRITICAL
        self._load_keyword()
        self.log = internalLog()
    def _redirect(self):
        self._stdout = sys.stdout
        sys.stdout = self.log
    def _recover(self):
        if self._stdout:
            sys.stdout = self._stdout
    def _load_keyword(self):
        keywords = self.keywordManager.get_keyword()
        for instanceName in keywords:
            for keywordName in keywords[instanceName]:
                if  vars(self).has_key(keywordName):
                    pass
                else:
                    vars(self)[keywordName] = keywords[instanceName][keywordName]

    def get_keyword(self,keywordName):
        keyword = self.keywordManager.get_keyword(keywordName)
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
        self._redirect()
        try:
            self._checkpoint()
        except Exception,e:
            # self.logger.error("testPoint `%s` failed, reason is %s"%(self.__class__.__name__,e))
            self.IMPACT.append("Throw Exception,reason is %s"%e)
            self.RCA.append(e)
            self.status = STATUS.FAIL
        finally:
            # self.logger.info("TestPoint(%s) result is [%s]" % (self.__class__.__name__, self.status))
            self._recover()

        self.RCA = RemoveDuplicates(self.RCA)
        self.IMPACT = RemoveDuplicates(self.IMPACT)
        internalLog = self.log.getContent()
        return self.passed,self.level,self.RCA,self.IMPACT,self.FIXSTEP,self.__doc__,internalLog




