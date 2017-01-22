import re
from manager import TestPointManagerInstance
from log.logger import logger
import pdb
from variable.variable import *
from library.library import parseRule
from output.output import OutPutQueue
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
    def run(self):
        self._introduceSelf()
        self._check_status()
        self._processResult()
        if not self.passed:
            selected = self.fix()
            return self.passed,selected
        else:
            return self.passed,CONTINUE
    def _introduceSelf(self):
        separator = "^"*80
        self._printf(separator)
        Note = "{Driver start to run the %s}:"%(self.__class__.__name__,)
        describe = "|\n*Description:  %s"%self.describe
        testPoint = "|\n*TestPoints:"
        self._printf(Note)
        self._printf(describe)
        self._printf(testPoint)
    def _processResult(self):
        #Result = "*Result:  Driver checked all related TestPoints,We can judge the Case is [%s]"%self.status
        Result = "|\n*Result: [%s]"%self.status
        self._printf(Result)
        self.logger.info("Case(%s) Rule is `%s`, result is [%s]"%(self.__class__.__name__,self.passCondition,self.status))

    def _interactive(self):
        Ask = "|\n*Question: What do you want to do next?(Yes/No)"
        Option = """
        * [Yes] Continue to the next Case.
        * [No] ReRun the Case Again."""
        Answer = "[Input Selected]:"
        select = ""
        self._printf(Ask)
        self._printf(Option)
        while 1:
            self._printf(Answer)
            answer = raw_input()
            answer = answer.lower()
            if answer.strip() == "yes" or answer.strip() == "y":
                select = CONTINUE
                break
            elif answer.strip() == "no" or answer.strip() == "n":
                select = RUNAGAIN
                break
            else:
                pass

        return select

    def fix(self):
        i = 1
        Steps = ""

        Note = "|\n*Fix Way: Fix it as below Step:\n|"
        self._printf(Note)
        for Step in self.fixStep:

            self._printf("|\t* Step %s. %s"%(i,Step))
            i += 1
        selected = self._interactive()
        return selected




if __name__ == "__main__":
    obj = _BaseCase()