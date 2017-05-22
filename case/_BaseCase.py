import re
from manager import TestPointManagerInstance
from log.logger import logger
import pdb,time
from variable.variable import *
from library.library import parseRule,RemoveDuplicates
from library.controlView import ControlView
from output.output import OutPutQueue
from configuration import ConfigManagerInstance
from exception.exception import CaseManagerException

class _BaseCase(object):
    def __init__(self):
        super(_BaseCase,self).__init__()
        self.passCondition = ""
        self.describe = "this is _BaseCase"
        #self.fixStep = ""
        self.logger = logger()
        self.status = NOTRUN
        self._ToPrint = True
        self._checkPointStatusDict = {}
        self._Impact = {}
        self._RCA = {}
        self._FixMethod = {}
        self.caseNumber = None
        self._internalCase = False

    def _printf(self,message):
        if self._ToPrint:
            OutPutQueue.put(message)
        while 1:
            if OutPutQueue.empty():
                break
    def _check_status(self):
        checkPointList = parseRule(self.passCondition)
        if len(checkPointList) >= 1:
            checkPointStatusDict = TestPointManagerInstance.run_test_points(checkPointList)
            self._checkPointStatusDict = checkPointStatusDict
            passCondition = self.passCondition
            for checkPoint in checkPointList:
                passCondition = passCondition.replace(checkPoint,str(checkPointStatusDict[checkPoint]["STATUS"]))
            status = eval(passCondition)
            if status:
                self.status = PASS
            else:
                self.status = FAIL
        else:
            self.logger.error("Case(%s) has not related testpoint"%self.__class__.__name__)

    @property
    def passed(self):
        return self.status == PASS
    def _readConfig(self):
        if self.caseNumber is None and self._internalCase is False:
            raise CaseManagerException("Exception :Case %s attribute caseNumber  is not set"%self.__class__.__name__)




    def run(self,RERUN=False):
        self._readConfig()
        self._check_status()
        self._LoadImpact()
        self._LoadRCA()
        self._LoadFixMethod()
        result = {"STATUS": self.passed,"IMPACT":self._Impact,"DESCRIPTION":self.describe,"RCA":self._RCA,"FIXMETHOD":self._FixMethod,"CASENUMBER":self.caseNumber}

        return result,CONTINUE


    def _LoadRCA(self):
        CriticalRCA = []
        NoCriticalRCA = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["RCA"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == CRITICAL:
                    CriticalRCA += self._checkPointStatusDict[TestPointName]["RCA"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == NOCRITICAL:
                    NoCriticalRCA += self._checkPointStatusDict[TestPointName]["RCA"]

        self._RCA = {"CriticalRCA":CriticalRCA,"NoCriticalRCA":NoCriticalRCA}
    def _InteractionClickedRCA(self):
        CriticalRCA = []
        NoCriticalRCA = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["RCA"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == CRITICAL:
                    CriticalRCA.append({"TestPointName":TestPointName,"RCA":self._checkPointStatusDict[TestPointName]["RCA"],"DESCRIBE":self._checkPointStatusDict[TestPointName]["DESCRIBE"]})
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == NOCRITICAL:
                    NoCriticalRCA.append({"TestPointName":TestPointName,"RCA":self._checkPointStatusDict[TestPointName]["RCA"],"DESCRIBE":self._checkPointStatusDict[TestPointName]["DESCRIBE"]})


        self._printf("|\n*Root Cause Analyzer:")
        if CriticalRCA:
            self._printf("|\n  \\--*Critical:")
            for RCA in CriticalRCA:

                self._printf("|\t\\--*For %s:"%RCA["TestPointName"] + "\n\t\t\\--*" + "\n\t\t\\--*".join(RCA["RCA"]))

        if NoCriticalRCA:
            self._printf("|\n  \\--*Minor:")
            for RCA in NoCriticalRCA:
                self._printf("|\t\\--*For %s:" % RCA["TestPointName"] + "\n\t\t\\--*" + "\n\t\t\\--*".join(RCA["RCA"]))


    def _LoadImpact(self):
        CriticalImpact = []
        NoCriticalImpact = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["IMPACT"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == CRITICAL:
                    CriticalImpact += self._checkPointStatusDict[TestPointName]["IMPACT"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == NOCRITICAL:
                    NoCriticalImpact += self._checkPointStatusDict[TestPointName]["IMPACT"]
        CriticalImpact = RemoveDuplicates(CriticalImpact)
        NoCriticalImpact = RemoveDuplicates(NoCriticalImpact)

        self._Impact =  {"CriticalImpact":CriticalImpact,"NoCriticalImpact":NoCriticalImpact}
    def _LoadFixMethod(self):
        CriticalFixMethod = []
        NoCriticalFixMethod = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["FIXSTEP"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == CRITICAL:
                    CriticalFixMethod  += self._checkPointStatusDict[TestPointName]["FIXSTEP"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == NOCRITICAL:
                    NoCriticalFixMethod += self._checkPointStatusDict[TestPointName]["FIXSTEP"]
        self._FixMethod = {"CriticalFixMethod":CriticalFixMethod,"NoCriticalFixMethod":NoCriticalFixMethod}







if __name__ == "__main__":
    obj = _BaseCase()