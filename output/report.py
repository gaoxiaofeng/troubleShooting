# -*- coding: utf-8 -*-
from output import OutPut
from library.controlView import ControlView
from manager import CaseManagerInstance
from variable.variable import  *
class report(object):
    def __init__(self):
        super(report,self).__init__()
        self.view = ControlView(width=58)
        self.caseResult =  CaseManagerInstance.case_record
        self.printf = OutPut().printf
    def write(self):
        _width = 18
        self._width = _width
        reportList = []
        _CaseList = []
        successReportList = []
        failureReportList = []
        i = 0
        for caseName in self.caseResult:
            # _caseName = caseName +  " "*(30 - len(caseName))
            _CaseList.append(caseName)
            caseStatus = self.caseResult[caseName]["STATUS"]
            if caseStatus:
                _Success = "Pass"
                _ShortCut = " "*((_width - 3)/2) + "[%s]"%i + " "*(_width - 3 - (_width - 3)/2)
                _CaseName = " "*((_width - len(caseName))/2) +  caseName + " "*(_width - len(caseName) - (_width - len(caseName))/2)
                _Result = " "*((_width - len(_Success))/2) + _Success + " "*(_width - len(_Success) - (_width - len(_Success))/2)
                report = "#%s#%s#%s#"%(_ShortCut,_CaseName,_Result)
                # report = "    [%s]    %sSuccess"%(i,_caseName)
                successReportList.append(caseName)
            else:
                _Failure = "(+)Fail"
                # report = "    [%s]    %sFailure (+)" % (i, _caseName)
                _ShortCut = " "*((_width - 3)/2) + "[%s]"%i + " "*(_width - 3 - (_width - 3)/2)
                _CaseName = " "*((_width - len(caseName))/2) +  caseName + " "*(_width - len(caseName) - (_width - len(caseName))/2)
                _Result = " "*((_width - len(_Failure))/2) + _Failure + " "*(_width - len(_Failure) - (_width - len(_Failure))/2)
                report = "#%s#%s#%s#"%(_ShortCut,_CaseName,_Result)
                failureReportList.append(caseName)
            reportList.append(report)
            i += 1
        reportList.append("#" + " " * ((_width - 3) / 2) + "[E]" + " " * (_width - 3 - (_width - 3) / 2) + "#" + " "*((_width - 4)/2) + "Exit" + " "*(_width - 4 - ((_width - 4)/2)) + "#")


        self.printf("*" * _width * 3 + "****")
        graph = """
          ____                        __
         / __ \___  ____  ____  _____/ /_
        / /_/ / _ \/ __ \/ __ \/ ___/ __/
       / _, _/  __/ /_/ / /_/ / /  / /_
      /_/ |_|\___/ .___/\____/_/   \__/
                /_/
        """
        self.printf(graph)

        # self.printf("*             Report             *")
        self.printf("*"*_width*3 + "****")
        left = " "*((_width - 6)/2)
        right = " "*(_width - 6 - (_width - 6)/2)
        graph = "*" + left + PRINT_BLUE + "Tested" + PRINT_END + right
        graph += "*" + left + PRINT_BLUE + "Passed" + PRINT_END + right
        graph += "*" + left + PRINT_BLUE + "Failed" + PRINT_END + right + "*"
        self.printf(graph)
        # self.printf("*%sTested%s*%sPassed%s*%sFailed%s*"%(left,right,left,right,left,right))
        self.printf("*" * _width*3 + "****")

        Tested = str(len(successReportList)+len(failureReportList))
        Tested = " "*((_width - len(Tested))/2) + Tested + " "*(_width - len(Tested)-(_width - len(Tested))/2)
        Passed = str(len(successReportList))
        Passed = " " * ((_width - len(Passed)) / 2 )+ PRINT_GREEN + Passed + PRINT_END + " " * (_width - len(Passed) - (_width - len(Passed)) / 2)
        Failed = str(len(failureReportList))
        Failed = " " * ((_width - len(Failed)) / 2) + PRINT_RED + Failed + PRINT_END + " " * (_width - len(Failed) - (_width - len(Failed)) / 2)

        self.printf("*%s*%s*%s*"%(Tested,Passed,Failed))
        self.printf("*" * _width * 3 + "****")
        self.printf(PRINT_YELLOW + "Cases List: The item containing `+` can be expanded." + PRINT_END)
        self.printf("*" * _width * 3 + "****")
        ShortCut = "ShortCut"
        ShortCut = " " * ((_width - len(ShortCut)) / 2) + ShortCut + " " * (_width - len(ShortCut) - (_width - len(ShortCut)) / 2)
        CaseName = "CaseName"
        CaseName = " " * ((_width - len(CaseName)) / 2) + CaseName + " " * (_width - len(CaseName) - (_width - len(CaseName)) / 2)
        Result = "Result"
        Result = " " * ((_width - len(Result)) / 2) + Result + " " * (_width - len(Result) - (_width - len(Result)) / 2)
        self.printf("*%s*%s*%s*"%(ShortCut,CaseName,Result))
        self.printf("*" * _width * 3 + "****")
        while 1:
            _choice = self.view(*reportList)
            if _choice == "e":
                break
            _choiceNo = int(_choice)
            if "+" not in reportList[_choiceNo] :
                continue

            selectedCaseName = _CaseList[_choiceNo]
            _selectedCaseStatus = self.caseResult[selectedCaseName]["STATUS"]
            self._caseDetailInfo(selectedCaseName)

    def _caseDetailInfo(self,caseName):
        status = self.caseResult[caseName]['STATUS']
        NoCriticalImpact = self.caseResult[caseName]['IMPACT']['NoCriticalImpact']
        CriticalImpact = self.caseResult[caseName]['IMPACT']['CriticalImpact']
        Description = self.caseResult[caseName]['DESCRIPTION']
        CriticalRCA =  self.caseResult[caseName]['RCA']['CriticalRCA']
        NoCriticalRCA =  self.caseResult[caseName]['RCA']['NoCriticalRCA']
        CriticalFixMethod = self.caseResult[caseName]['FIXMETHOD']['CriticalFixMethod']
        NoCriticalFixMethod = self.caseResult[caseName]['FIXMETHOD']['NoCriticalFixMethod']

        self.printf("*"*(self._width*3+4))
        self.printf("|*CaseName:\t{%s}"%caseName)

        if isinstance(Description,list):
            Description = "\n".join(Description)
        self.printf("|*Description:  %s" % Description)
        self.printf("|*Impact Analysis:")
        if CriticalImpact or NoCriticalImpact:
            for _Impact in CriticalImpact:
                self.printf("|\t[Critical] | %s"%_Impact)

            for _Impact in NoCriticalImpact:
                self.printf("|\t[Minor]    | %s"%_Impact)

        self.printf("|*Root Cause Analysis:")
        if CriticalRCA or NoCriticalRCA:
            for _RCA in CriticalRCA:
                if "\n" in _RCA:
                    _RCA = _RCA.replace("\n","\n|")
                self.printf("|\t[Critical] | %s"%_RCA)
            for _RCA in NoCriticalRCA:
                if "\n" in _RCA:
                    _RCA = _RCA.replace("\n","\n|")
                self.printf("|\t[Minor]    | %s"%_RCA)


        self.printf("|*Fix Method:")
        if CriticalFixMethod:
            self.printf("|\t*Fix Method for Critical Problems:")
            i = 1
            for _Method in CriticalFixMethod:
                if "\n" in _Method:
                    _Method = _Method.replace("\n","\n|")
                self.printf("|\t\t(Step %s). %s"%(i,_Method))
                i += 1


        if NoCriticalFixMethod:
            self.printf("|\t*Fix Method for Minor Problems:")
            i = 1
            for _Method in NoCriticalFixMethod:
                if "\n" in _Method:
                    _Method = _Method.replace("\n","\n|")
                self.printf("|\t\tStep %s. %s"%(i,_Method))
                i += 1
        self.printf("*" * (self._width * 3 + 4))

    def __del__(self):
        graph = "Bye-bye!"
        self.printf(graph)


