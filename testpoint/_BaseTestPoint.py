from log.logger import logger
from variable.variable import *
from output.output import OutPutQueue
from library.library import parseRule
from manager import TestPointManager
from configuration import  ConfigManagerInstance
class _BaseTestPoint(object):
    def __init__(self):
        super(_BaseTestPoint,self).__init__()
        self.describe = "this is _BaseTestPoint"
        self.ToPrint = False
        self.logger = logger()
        self.status = NOTRUN
        self._ToPrint = True
        self._firstTestPoint = True
        self.RCA = []
        self.IMPACT = []
        self.FIXSTEP = []
        self.level = NOCRITICAL
    def _printf(self,message):
        if self._ToPrint:
            OutPutQueue.put(message)

    def _checkpoint(self):
        pass

    @property
    def passed(self):
        return self.status == PASS

    def _interactive(self):
        if self._ToPrint:
            if self._firstTestPoint:
                self._printf("|\n*TestPoints:")
            self._printf("|\t|\n|\t\\--*[%s] %s "%(self.status,self.describe,))
    def readConfig(self):
        self.runMode = ConfigManagerInstance.config["runMode"]
        if self.runMode == SingleMode:
            self._ToPrint = False
    def _initBeforeRun(self):
        self.RCA = []
        self.IMPACT = []
        self.FIXSTEP = []
    def run(self,firstTestPoint=True):
        self._firstTestPoint = firstTestPoint
        self._initBeforeRun()
        self.readConfig()
        self._checkpoint()
        self.logger.info("TestPoint(%s) result is [%s]"%(self.__class__.__name__,self.status))
        self._interactive()
        return self.passed,self.level,self.RCA,self.IMPACT,self.FIXSTEP,self.describe





