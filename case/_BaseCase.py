# -*- coding: utf-8 -*-
# import re
from framework.modules.manager import ManagerFactory
from framework.log.logger import logger
# import pdb,time
from framework.variable.variable import *
from framework.libraries.library import parseRule,RemoveDuplicates
# from framework.libraries.controlView import ControlView
from framework.output.output import OutPutQueue
# from framework.modules.configuration import ConfigManagerInstance
from framework.exception.exception import CaseManagerException

class _BaseCase(object):
    """
    this is basecase class.
    """
    def __init__(self):
        super(_BaseCase,self).__init__()
        self.passCondition = None
        #self.fixStep = ""
        self.logger = logger()
        self.status = STATUS.NOTRUN
        self._ToPrint = True
        self._checkPointStatusDict = {}
        self._Impact = {}
        self._RCA = {}
        self._FixMethod = {}
        self.caseNumber = None
        self.referenceDocument = None

    def _printf(self,message):
        if self._ToPrint:
            OutPutQueue.put(message)
        while 1:
            if OutPutQueue.empty():
                break
    def _check_status(self):
        checkPointList = parseRule(self.passCondition)
        if len(checkPointList) >= 1:
            TestPointManagerInstance = ManagerFactory().getManager(LAYER.TestPoint)
            checkPointStatusDict = TestPointManagerInstance.run_test_points(checkPointList)
            self._checkPointStatusDict = checkPointStatusDict
            passCondition = self.passCondition
            for checkPoint in checkPointList:
                passCondition = passCondition.replace(checkPoint,str(checkPointStatusDict[checkPoint]["STATUS"]))
            status = eval(passCondition)
            if status:
                self.status = STATUS.PASS
            else:
                self.status = STATUS.FAIL
        else:
            self.logger.error("Case(%s) has not related testpoint"%self.__class__.__name__)

    @property
    def passed(self):
        return self.status == STATUS.PASS
    def _readConfig(self):
        if self.passCondition is None:
            raise CaseManagerException("Case(%s) has not define passCondition! "%self.__class__.__name__)




    def run(self,RERUN=False):
        self._readConfig()
        self._check_status()
        self._SetFailureLevel()
        self._LoadImpact()
        self._LoadRCA()
        self._LoadFixMethod()
        result = {"STATUS": self.passed,"FAILURELEVEL":self.FailureLevel,"IMPACT":self._Impact,"DESCRIPTION":self.__doc__.strip() if self.__doc__ is not None else self.__doc__,"RCA":self._RCA,"FIXMETHOD":self._FixMethod,"REFERENCE":self.referenceDocument,"TESTPOINT":self._checkPointStatusDict}

        return result,BEHAVIOR.CONTINUE
    def _SetFailureLevel(self):
        _level = None
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["STATUS"] is False:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] is LEVEL.CRITICAL:
                    _level = LEVEL.CRITICAL
                    break
                else:
                    _level = LEVEL.NOCRITICAL
        self.FailureLevel = _level



    def _LoadRCA(self):
        CriticalRCA = []
        NoCriticalRCA = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["RCA"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.CRITICAL:
                    CriticalRCA += self._checkPointStatusDict[TestPointName]["RCA"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.NOCRITICAL:
                    NoCriticalRCA += self._checkPointStatusDict[TestPointName]["RCA"]

        self._RCA = {"CriticalRCA":CriticalRCA,"NoCriticalRCA":NoCriticalRCA}
    def _InteractionClickedRCA(self):
        CriticalRCA = []
        NoCriticalRCA = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["RCA"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.CRITICAL:
                    CriticalRCA.append({"TestPointName":TestPointName,"RCA":self._checkPointStatusDict[TestPointName]["RCA"],"DESCRIBE":self._checkPointStatusDict[TestPointName]["DESCRIBE"]})
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.NOCRITICAL:
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
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.CRITICAL:
                    CriticalImpact += self._checkPointStatusDict[TestPointName]["IMPACT"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.NOCRITICAL:
                    NoCriticalImpact += self._checkPointStatusDict[TestPointName]["IMPACT"]
        CriticalImpact = RemoveDuplicates(CriticalImpact)
        NoCriticalImpact = RemoveDuplicates(NoCriticalImpact)

        self._Impact =  {"CriticalImpact":CriticalImpact,"NoCriticalImpact":NoCriticalImpact}
    def _LoadFixMethod(self):
        CriticalFixMethod = []
        NoCriticalFixMethod = []
        for TestPointName in self._checkPointStatusDict:
            if self._checkPointStatusDict[TestPointName]["FIXSTEP"]:
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.CRITICAL:
                    CriticalFixMethod  += self._checkPointStatusDict[TestPointName]["FIXSTEP"]
                if self._checkPointStatusDict[TestPointName]["LEVEL"] == LEVEL.NOCRITICAL:
                    NoCriticalFixMethod += self._checkPointStatusDict[TestPointName]["FIXSTEP"]


        self._FixMethod = {"CriticalFixMethod":CriticalFixMethod,"NoCriticalFixMethod":NoCriticalFixMethod}







if __name__ == "__main__":
    obj = _BaseCase()