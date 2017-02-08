from log.logger import logger
from exception.exception import *
import re
from variable.variable import *

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
            #self.logger.info("%s.register instance %s"%(self.__class__.__name__, className))
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







class  TestPointManager(BaseManager):
    def __init__(self):
        super(TestPointManager,self).__init__()
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
            testPointfull = "%s.%s"%(testPoint,"run")
            testPointRunner = self.get_keyword(testPointfull)
            status,rcaList,impactList,fixStepList = testPointRunner(firstTestPoint)
            if firstTestPoint:
                firstTestPoint = False
            #statusDict["{%s}"%testPoint]=status
            statusDict["{%s}" % testPoint] = {"STATUS":status,"RCA":rcaList,"IMPACT":impactList,"FIXSTEP":fixStepList}
            #{"Security_001":{"STATUS":True,"RCA":[,],"IMPACT":[,]}}
        self.testPoint_record = statusDict
        return statusDict

    @property
    def testPoint_record(self):
        return self.__testPoint_record
    @testPoint_record.setter
    def testPoint_record(self,testPoint_record):
        for testPointName in testPoint_record:
            self.__testPoint_record[testPointName] = testPoint_record[testPointName]


class  EngineManager(BaseManager):
    def __init__(self):
        super(EngineManager,self).__init__()


class CaseManager(BaseManager):
    def __init__(self):
        super(CaseManager,self).__init__()
        self.__case_record = {}
    def run_case(self,case):
        RERUN = False
        caseRunnerEntry = "%s.%s"%(case,"run")
        caseRunner = self.get_keyword(caseRunnerEntry)
        while 1:
            status,behavior = caseRunner(RERUN)
            if behavior == CONTINUE:
                break
            elif behavior == RUNAGAIN:
                RERUN = True
            elif behavior == EXIT:
                break
            elif behavior == DONEFIXED:
                RERUN = True

            else:
                raise CaseManagerException("unsupport behavior : %s"%behavior)

        self.case_record = {case:status}
        return  status,behavior
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

TestPointManagerInstance = TestPointManager()
EngineManagerInstance =  EngineManager()
CaseManagerInstance = CaseManager()
if __name__ == "__main__":
    pass





