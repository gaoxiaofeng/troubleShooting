# -*- coding: utf-8 -*-
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.output.output import OutPutQueue
from troubleshooting.framework.libraries.library import parseRule,RemoveDuplicates
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.log.internalLog import internalLog
from threading import Thread
import traceback
try:
    #import project config.variable
    from config.variable import *
except:
    print "WARN: failed to import config.variable"
import sys
class TestPoint(Thread):
    def __init__(self):
        super(TestPoint,self).__init__()
        self.keywordManager = ManagerFactory().getManager(LAYER.KeyWords)
        self.logger = logger()
        self.status = STATUS.NOTRUN
        self._ToPrint = True
        self._firstTestPoint = True
        self.RCA = []
        self.IMPACT = []
        self.FIXSTEP = []
        self.AUTOFIEXSTEP = []
        self.level = LEVEL.NOCRITICAL
        self._load_keyword()
        self.log = internalLog()
        self.timeout = "30s"
        self.internalLog = ""
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

    def get_attribute(self,attribute):
        if  self.__dict__.has_key(attribute):
            return self.__dict__[attribute]
        else:
            raise Exception("%s has not attribute %s"%(self.__class__.__name__,attribute))
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
            self.IMPACT.append("TestPoint Throw Exception!")
            self.RCA.append(traceback.format_exc())
            self.status = STATUS.FAIL
        finally:
            # self.logger.info("TestPoint(%s) result is [%s]" % (self.__class__.__name__, self.status))
            self._recover()

        self.RCA = RemoveDuplicates(self.RCA)
        self.IMPACT = RemoveDuplicates(self.IMPACT)
        self.internalLog = self.log.getContent()
        # return self.passed,self.level,self.RCA,self.IMPACT,self.FIXSTEP,self.__doc__,self.internalLog

    def getResult(self):
        if self.isAlive():
            return
        else:
            return self.passed, self.RCA, self.IMPACT, self.FIXSTEP,self.AUTOFIEXSTEP,"" if self.__doc__ is  None else self.__doc__.strip(), self.internalLog

    def terminate(self):
        raise RuntimeError("raise SystemExit from terminate commands")

