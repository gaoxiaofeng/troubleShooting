from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.variable.variable import *

def filterCaselist(caseNameList):
    caseNameList_NeedRun = []
    CaseManagerInstance = ManagerFactory().getManager(LAYER.Case)
    for caseName in caseNameList:
        NeedRun = CaseManagerInstance.is_need_to_run(caseName)
        if NeedRun:
            caseNameList_NeedRun.append(caseName)
    return caseNameList_NeedRun

