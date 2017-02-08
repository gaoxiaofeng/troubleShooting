import re
from manager import TestPointManagerInstance
from log.logger import logger
import pdb,time
from variable.variable import *
from library.library import parseRule
from library.controlView import ControlView
from output.output import OutPutQueue
from configuration import ConfigManagerInstance
class _BaseCase(object):
    def __init__(self):
        super(_BaseCase,self).__init__()
        self.passCondition = ""
        self.describe = "this is _BaseCase"
        self.fixStep = ""
        self.logger = logger()
        self.status = NOTRUN
        self._ToPrint = True

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
            passCondition = self.passCondition
            for checkPoint in checkPointList:
                passCondition = passCondition.replace(checkPoint,str(checkPointStatusDict[checkPoint]))
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
        pass

    def run(self,RERUN=False):
        self._readConfig()
        if RERUN is False:
            self._introduceSelf()
        self._check_status()
        self._processResult()
        if not self.passed:
            while 1:

                selected = self._InteractionAfterProblemBeObserved()
                if selected == TRYFIXED:
                    selected = self.fixManually()
                    if selected == DONEFIXED or selected == EXIT:
                        break


                else:
                    break


            return self.passed,selected
        else:
            return self.passed,CONTINUE
    def _introduceSelf(self):
        separator = "^"*80
        self._printf(separator)
        Note = "{Driver start to run the %s}:"%(self.__class__.__name__,)
        describe = "|\n*Description:  %s"%self.describe
        self._printf(Note)
        self._printf(describe)
    def _processResult(self):
        #Result = "*Result:  Driver checked all related TestPoints,We can judge the Case is [%s]"%self.status
        Result = "|\n*Result: [%s]"%self.status
        self._printf(Result)
        self.logger.info("Case(%s) Rule is `%s`, result is [%s]"%(self.__class__.__name__,self.passCondition,self.status))


    def _InteractionAfterProblemBeFixed(self):
        Question = "|\n*Question: Do you have performed the above fixed steps?"
        self._printf(Question)
        view = ControlView()
        chLower = view("[Y] Yes ","[N] No ","[E] Exit Tool ")
        if chLower == "y":
            select = DONEFIXED
        elif chLower == "n":
            select = NEVERFIXED
        elif chLower == "e":
            select = EXIT
        else:
            raise BaseException("unkown selected result :%s"%chLower)

        return select
    def _InteractionAfterProblemBeObserved(self):
        Question = "|\n*Question: A Problem be observed, What's the next step?"
        self._printf(Question)
        view = ControlView()
        chLower = view("[N] Ignore, Next Case ","[D] Detail Info","[F] Try To Fixed ","[R] Re-Check Again ","[E] Exit Tool ")
        if chLower == "n":
            select = CONTINUE
        elif chLower == "r":
            select = RUNAGAIN
        elif chLower == "e":
            select = EXIT
        elif chLower == "f":
            select = TRYFIXED
        elif chLower == "d":
            select = CONTINUE
        else:
            raise BaseException("unkown selected result :%s"%chLower)

        return select
    def fixManually(self):
        i = 1
        Steps = ""

        Note = "|\n*Fixed Steps: \n|"
        self._printf(Note)
        for Step in self.fixStep:

            self._printf("|\t* Step %s. %s"%(i,Step))
            i += 1
        selected = self._InteractionAfterProblemBeFixed()

        return  selected






if __name__ == "__main__":
    obj = _BaseCase()