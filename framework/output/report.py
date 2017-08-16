# -*- coding: utf-8 -*-
from framework.output.output import OutPut
from framework.libraries.controlView import ControlView
from framework.libraries.library import singleton
from framework.manager import ManagerFactory
from framework.variable.variable import  *
from framework.configuration import ConfigManagerInstance
from framework.output.writehtml import html
@singleton
class report(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.view = ControlView(width=58)
        self.caseResult =  ManagerFactory().getManager(LAYER.Case).case_record
        self.printf = OutPut().printf
    def console(self):
        if not ConfigManagerInstance.config["Print"]:
            return
        _width = ConfigManagerInstance.config["report_table_width"]
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
                level = self.caseResult[caseName]["FAILURELEVEL"]

                _Failure = "(+)Fail" if level is LEVEL.CRITICAL else "(+)Warn"
                # report = "    [%s]    %sFailure (+)" % (i, _caseName)
                _ShortCut = " "*((_width - 3)/2) + "[%s]"%i + " "*(_width - 3 - (_width - 3)/2)
                _CaseName = " "*((_width - len(caseName))/2) +  caseName + " "*(_width - len(caseName) - (_width - len(caseName))/2)
                _Result = " "*((_width - len(_Failure))/2) + _Failure + " "*(_width - len(_Failure) - (_width - len(_Failure))/2)
                report = "#%s#%s#%s#"%(_ShortCut,_CaseName,_Result)
                failureReportList.append(caseName)
            reportList.append(report)
            i += 1
        reportList.append("#" + " " * ((_width - 3) / 2) + "[E]" + " " * (_width - 3 - (_width - 3) / 2) + "#" + " "*((_width - 4)/2) + "Exit" + " "*(_width - 4 - ((_width - 4)/2)) + "#" + " "*_width + "#")


        self.printf("*" * _width * 3 + "****")
        graph = r"""
          ____                        __
         / __ \___  ____  ____  _____/ /_
        / /_/ / _ \/ __ \/ __ \/ ___/ __/
       / _, _/  __/ /_/ / /_/ / /  / /_
      /_/ \_\\___/ .___/\____/_/   \__/
                /_/
        """
        graph="""
     ____  ____  ____  _____  ____  ____
    (  _ \( ___)(  _ \(  _  )(  _ \(_  _)
     )   / )__)  )___/ )(_)(  )   /  )(
    (_)\_)(____)(__)  (_____)(_)\_) (__)
        """
        self.printf(graph)

        # self.printf("*             Report             *")
        self.printf("*"*_width*3 + "****")
        left = " "*((_width - 6)/2)
        right = " "*(_width - 6 - (_width - 6)/2)
        graph = "*" + left + COLOUR.Blue + "Tested" + COLOUR.End + right
        graph += "*" + left + COLOUR.Blue + "Passed" + COLOUR.End + right
        graph += "*" + left + COLOUR.Blue + "Failed" + COLOUR.End + right + "*"
        self.printf(graph)
        # self.printf("*%sTested%s*%sPassed%s*%sFailed%s*"%(left,right,left,right,left,right))
        self.printf("*" * _width*3 + "****")

        Tested = str(len(successReportList)+len(failureReportList))
        Tested = " "*((_width - len(Tested))/2) + Tested + " "*(_width - len(Tested)-(_width - len(Tested))/2)
        Passed = str(len(successReportList))
        Passed = " " * ((_width - len(Passed)) / 2 )+ COLOUR.Green + Passed + COLOUR.End + " " * (_width - len(Passed) - (_width - len(Passed)) / 2)
        Failed = str(len(failureReportList))
        Failed = " " * ((_width - len(Failed)) / 2) + COLOUR.Red + Failed + COLOUR.End + " " * (_width - len(Failed) - (_width - len(Failed)) / 2)

        self.printf("*%s*%s*%s*"%(Tested,Passed,Failed))
        self.printf("*" * _width * 3 + "****")
        _title = "Case Deail List"
        self.printf("*" + " "*((_width*3 +2 - len(_title))/2) + _title + " "*((_width*3 +2) - len(_title) - ((_width*3 +2 - len(_title))/2)) + "*")
        _title = "The item containing `+` can be expanded."
        self.printf("*" + COLOUR.Yellow + _title + COLOUR.End + " "* +(_width*3+2-len(_title)) + "*")
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
        ReferenceDocument = self.caseResult[caseName]['REFERENCE']
        self.printf("*"*(self._width*3+4))
        self.printf("|*CaseName:\t{%s}"%caseName)

        if ReferenceDocument:
            self.printf("|*Reference document: %s"%ReferenceDocument)
        if Description is not None:
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
        self.printf("|\t*Please refer to ./report.html")
        # if CriticalFixMethod:
        #     self.printf("|\t*Fix Method for Critical Problems:")
        #     i = 1
        #     for _Method in CriticalFixMethod:
        #         if "\n" in _Method:
        #             _Method = _Method.replace("\n","\n|")
        #         self.printf("|\t\tStep %s. %s"%(i,_Method))
        #         i += 1
        #
        #
        # if NoCriticalFixMethod:
        #     self.printf("|\t*Fix Method for Minor Problems:")
        #     i = 1
        #     for _Method in NoCriticalFixMethod:
        #         if "\n" in _Method:
        #             _Method = _Method.replace("\n","\n|")
        #         self.printf("|\t\tStep %s. %s"%(i,_Method))
        #         i += 1
        self.printf("*" * (self._width * 3 + 4))
    def writeReport(self):
        html().write()
        graph = """The Report was saved as ./report.html"""
        self.printf(graph)



