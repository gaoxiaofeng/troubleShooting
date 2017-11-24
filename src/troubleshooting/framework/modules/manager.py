# -*- coding: utf-8 -*-
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.exception.exception import *
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.libraries.library import singleton,convertTime
from troubleshooting.framework.modules.configuration import ConfigManagerInstance
from troubleshooting.framework.modules.tags import TagPattern
import sys,os
import time
class BaseManager(object):
    '''
    base manager
    '''
    def __init__(self):
        super(BaseManager,self).__init__()
        self.logger = logger()
        self.__registry = {}


    def __str__(self):
        return "%s dict:%s"%(self.__class__.__name__,self.__dict__)
    __repr__ = __str__
    @property
    def _registry(self):
        return self.__registry
    @_registry.setter
    def _registry(self,instance):
        className =  instance.__class__.__name__
        if self.__registry.has_key(className):
            self.logger.error("repeat register instance %s"%className)
        else:
            instanceMethod = self._parse_instance(instance)
            self.__registry[className] = instanceMethod
    def register(self,instance):
        """
        register the class.
        """
        if isinstance(instance,(type,)):
            self._registry = instance()
        elif isinstance(instance,(object,)):
            self._registry = instance
        else:
            raise BaseManagerException("BaseManager.register: args must be a class/object.")
    def _parse_instance(self,instance):
        instaceMethod = {}
        for attr in dir(instance):
            if not attr.startswith("_"):
                keyword = getattr(instance,attr)
                if  callable(keyword):
                    instaceMethod[attr] = keyword

        return instaceMethod
    def get_keyword(self,keywordName=None):
        if keywordName == None:
            return  self._registry
        #pdb.set_trace()
        findNullError = "search keyword null, keyword:[%s]"%keywordName

        if "." in keywordName:
            if keywordName.count(".") != 1:
                raise BaseManagerException(findNullError)

            instance = keywordName.split(".")[0].strip()
            instanceMethod = keywordName.split(".")[-1].strip()

            if self._registry.has_key(instance) and self._registry[instance].has_key(instanceMethod):
                keyword = self._registry[instance][instanceMethod]
                return keyword
            else:
                raise BaseManagerException(findNullError)
        else:
            keywordList = []
            for instanceName in self._registry:
                if self._registry[instanceName].has_key(keywordName):
                    keywordList.append(self._registry[instanceName][keywordName])
            if len(keywordList) == 0:
                raise BaseManagerException(findNullError)
            elif len(keywordList) == 1:
                keyword = keywordList[0]
                return keyword
            else:
                findMultiError =  "search keyword multi, keyword:%s,result:%s"%(keywordName,keywordList)
                raise BaseManagerException(findMultiError)

@singleton
class  TestPointManager(BaseManager):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.__testPoint_record = {}
    def run_test_points(self,testPointList):

        statusDict = {}
        if not isinstance(testPointList,list):
            testPointList = [testPointList]
        firstTestPoint = True
        for testPoint in testPointList:

            if "{" in testPoint:
                testPoint = testPoint.strip("{")
            if "}" in testPoint:
                testPoint = testPoint.strip("}")
            testPointRunner = self.get_keyword("%s.%s"%(testPoint,"start"))
            testPointGetResult = self.get_keyword("%s.%s"%(testPoint,"getResult"))
            testPointIsAlive =  self.get_keyword("%s.%s"%(testPoint,"isAlive"))
            testPointKill = self.get_keyword("%s.%s"%(testPoint,"terminate"))
            testPointWaitForExist = self.get_keyword("%s.%s"%(testPoint,"join"))
            testPointAttribute = self.get_keyword("%s.%s"%(testPoint,"get_attribute"))
            testPointTimeout = testPointAttribute("timeout")
            testPointLevel =  testPointAttribute("level")
            start_time = time.time()
            expiration_time = start_time + convertTime(testPointTimeout)
            # testPointRunner(firstTestPoint)
            testPointRunner()
            while time.time() < expiration_time:
                result = testPointGetResult()
                if result is not None:
                    status,rcaList,impactList,fixStepList,autoFixStepList,describe,internalLog = result
                    break
            end_time = time.time()
            cost_time = float("%.2f"%(end_time - start_time))
            cost_time_string = "%s sec"%cost_time
            if result is None:
                if testPointIsAlive():
                    try:
                        testPointKill()
                    except Exception,e:
                        print e
                    finally:
                        testPointWaitForExist()
                status, rcaList, impactList, fixStepList,autoFixStepList, describe, internalLog = False,["testpoint running timeout [%s]"%testPointTimeout],[],[],[],"",""
            if firstTestPoint:
                firstTestPoint = False
            statusDict["{%s}" % testPoint] = {"STATUS":status,"RCA":rcaList,"IMPACT":impactList,"FIXSTEP":fixStepList,"AUTOFIXSTEP":autoFixStepList,"LEVEL":testPointLevel,"DESCRIBE":describe,"LOG":internalLog,"TIMEOUT":testPointTimeout,"COST":cost_time_string}
            #{"Security_001":{"STATUS":True,"RCA":[,],"IMPACT":[,],"FIXSTEP":[],"LEVEL":"XXXX","DESCRIBE":"xxxx"}}
        self.testPoint_record = statusDict
        return statusDict

    @property
    def testPoint_record(self):
        return self.__testPoint_record
    @testPoint_record.setter
    def testPoint_record(self,testPoint_record):
        for testPointName in testPoint_record:
            self.__testPoint_record[testPointName] = testPoint_record[testPointName]
@singleton
class  KeywordManager(BaseManager):
    def __init__(self):
        super(self.__class__,self).__init__()

@singleton
class  RecoveryManager(BaseManager):
    def __init__(self):
        super(self.__class__,self).__init__()
    def run_recovery(self,recovery,*args):

        recoveryRunnerEntry = "%s.%s"%(recovery,"run")
        recoveryRunner = self.get_keyword(recoveryRunnerEntry)
        result,Log = recoveryRunner(*args)

        return result,Log



@singleton
class CaseManager(BaseManager):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.__case_record = {}
    def run_case(self,case):
        RERUN = False
        if ConfigManagerInstance.config["Case"]:
            if ConfigManagerInstance.config["Case"] != case:
                return  BEHAVIOR.CONTINUE
        if ConfigManagerInstance.config["Include"]:
            #process include tags
            patterns = ConfigManagerInstance.config["Include"]
            tags = self.get_keyword("%s.getTags"%case)()
            if not TagPattern(patterns).match(tags):
                return BEHAVIOR.CONTINUE

        if ConfigManagerInstance.config["Exclude"]:
            #process exclude tags
            patterns = ConfigManagerInstance.config["Exclude"]
            tags = self.get_keyword("%s.getTags"%case)()
            if TagPattern(patterns).match(tags):
                return BEHAVIOR.CONTINUE
        caseRunnerEntry = "%s.%s"%(case,"run")
        caseRunner = self.get_keyword(caseRunnerEntry)
        while 1:
            if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                print "-" * 40
                sys.stdout.write(r"%25s"%case)
            result,behavior = caseRunner(RERUN)
            if ConfigManagerInstance.config["SYSTEM"] == SYSTEM.WINDOWS.value:
                sys.stdout.write(r"%15s"%("Done"+os.linesep))
                print "-" * 40
            if behavior == BEHAVIOR.CONTINUE:
                break
            elif behavior == BEHAVIOR.RUNAGAIN:
                RERUN = True
            elif behavior == BEHAVIOR.EXIT:
                break
            else:
                raise CaseManagerException("unsupport behavior : %s"%behavior)

        self.case_record = {case:result}
        return  behavior


    def is_need_to_run(self,case):
        if ConfigManagerInstance.config["Case"]:
            if ConfigManagerInstance.config["Case"] != case:
                return False

        if ConfigManagerInstance.config["Include"]:
            #process include tags
            patterns = ConfigManagerInstance.config["Include"]
            tags = self.get_keyword("%s.getTags"%case)()
            if not TagPattern(patterns).match(tags):
                return False

        if ConfigManagerInstance.config["Exclude"]:
            #process exclude tags
            patterns = ConfigManagerInstance.config["Exclude"]
            tags = self.get_keyword("%s.getTags"%case)()
            if TagPattern(patterns).match(tags):
                return False

        return  True
    @property
    def case_record(self):
        return self.__case_record
    @case_record.setter
    def case_record(self,case_record):
        for caseName in case_record:

            if self.__case_record.has_key(caseName):
                self.logger.info("repeat record case %s"%(caseName,))
            else:
                self.__case_record[caseName] = case_record[caseName]

class ManagerFactory(object):
    def __init__(self):
        super(ManagerFactory,self).__init__()
    def getManager(self,name):
        if name == LAYER.KeyWords:
            return  KeywordManager()
        elif name == LAYER.TestPoint:
            return  TestPointManager()
        elif name == LAYER.Case:
            return  CaseManager()
        elif name == LAYER.Recovery:
            return RecoveryManager()
        else:
            return  None

if __name__ == "__main__":
    pass





