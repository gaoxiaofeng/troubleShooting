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
            self._printf("|\t|\n|\t\\--*[%s] %s "%(self.status,self.describe,))
    def readConfig(self):
        self.runMode = ConfigManagerInstance.config["runMode"]
        if self.runMode == SingleMode:
            self._ToPrint = False

    def run(self):
        self.readConfig()
        self._checkpoint()
        self.logger.info("TestPoint(%s) result is [%s]"%(self.__class__.__name__,self.status))
        self._interactive()
        return self.passed





