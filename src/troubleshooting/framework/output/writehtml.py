# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.libraries.library import list2stringAndFormat
from troubleshooting.framework.libraries.system import createDir
from troubleshooting.framework.modules.configuration import ConfigManagerInstance
from troubleshooting.framework.output.Print import CONSOLE
import time
import os,sys
from os.path import  join,abspath,dirname
from htmltemplate import *
import re
class html(object):
    def __init__(self):
        super(html,self).__init__()
        self.caseResult = ManagerFactory().getManager(LAYER.Case).case_record
        self.currenttime = time.strftime("%Y-%m-%d %X %Z",time.localtime())
    def write(self):
        data = ""
        data += HTML_BEFORE
        data += HTML_HEAD
        data +="""
<body bgcolor = "#E9EAEE">
<h1 align="center">TroubleShooting Framework Report</h1>
<p><i>%s</i></p>
	<table width="100%%" border="2" class="bordered">
		<thead>
			<tr ><th width="15%%">CaseName</th><th width="5%%" >Status</th><th width="80%%">Attribute</th></tr>
		</thead>
		<tbody>
"""%(self.currenttime,)
        recovery_id = 1
        for i,caseName in enumerate(self.caseResult):
            i += 1
            caseStatus = self.caseResult[caseName]["STATUS"]
            DESCRIPTION = self.caseResult[caseName]["DESCRIPTION"]
            REFERENCE = self.caseResult[caseName]["REFERENCE"]
            REFERENCEHtml = '<a href="%s">reference document</>'%REFERENCE if REFERENCE else '<font color="#d0d0d0">NA</font>'
            TAGS = self.caseResult[caseName]["TAGS"]
            TESTPOINT = self.caseResult[caseName]["TESTPOINT"]
            parent_pass = """
            <tr  bgcolor="#53C579" class="parent" id="row_0%s"><td colspan="1">%s</td><td>PASS</td><td colspan="1"></td></tr>"""%(i,caseName,)
            parent_fail = """
            <tr  bgcolor="#FF3030" class="parent" id="row_0%s"><td colspan="1">%s</td><td>FAIL</td><td colspan="1"></td></tr>"""%(i,caseName,)
            parent_warn = """
            <tr  bgcolor="#FF7F00" class="parent" id="row_0%s"><td colspan="1">%s</td><td>WARN</td><td colspan="1"></td></tr>"""%(i,caseName,)
            if caseStatus:
                data += parent_pass
            else:
                _level = self.caseResult[caseName]["LEVEL"]
                if _level is LEVEL.CRITICAL:
                    data += parent_fail
                else:
                    data += parent_warn

            data += """
            <tr class="child_row_0%s" style="display:none"><td>Description</td><td></td><td>%s</td></tr>
            <tr class="child_row_0%s" style="display:none"><td>Reference</td><td></td><td>%s</td></tr>
            <tr class="child_row_0%s" style="display:none"><td>Tags</td><td></td><td>%s</td></tr>
"""%(i,DESCRIPTION,i,REFERENCEHtml,i,TAGS)

            data += """
            <tr class="child_row_0%s" style="display:none">
            <td colspan="3" >
                <table border="1"  width="100%%" style="margin:0px">            
            """%i
            data += """
                    <tr>
                            <th width="5%%">
                                <b>TestPoint</b>
                            </th>  
                            <th width="5%%">
                                <b>Status</b>
                            </th>                                               
                            <th width="5%%">
                                <b>Level</b>
                            </th>
                            <th width="15%%" name="nolog">
                               <b>Impact</b>
                            </th>
                            <th width="35%%" name="nolog">
                               <b>Root Cause</b>
                            </th>
                            <th width="15%%" name="nolog">
                               <b>Fix Method</b>
                            </th>
                            <th width="20%%" name="nolog">
                               <b>Auto Fix Method</b>
                            </th>
                            <th style="display:none;" width="85%%" name="log">
                               <b>LOG</b>
                            </th>
                    </tr>            
                    """
            for testpoint in TESTPOINT:
                testpointStatus = TESTPOINT[testpoint]["STATUS"]
                testpointStatusHtml = '<font color="green"><b><i>%s</i></b></font>' % STATUS.PASS.value.lower() if testpointStatus else '<font color="red"><b><i>%s</i></b></font>' % STATUS.FAIL.value.lower()
                testpointImpact = TESTPOINT[testpoint]["IMPACT"]
                testpointImpact = list2stringAndFormat(testpointImpact)
                if not testpointImpact:
                    testpointImpact = '<font color="#d0d0d0">NA</font>'
                testpointImpactHtml = testpointImpact.replace("\n","</br>")
                testpointLevel =  TESTPOINT[testpoint]["LEVEL"]
                testpointLevelHtml = testpointLevel.value
                testpointDescribe = TESTPOINT[testpoint]["DESCRIBE"]
                testpointRCA = TESTPOINT[testpoint]["RCA"]
                testpointRCA = list2stringAndFormat(testpointRCA)
                if not testpointRCA:
                    testpointRCA = '<font color="#d0d0d0">NA</font>'
                testpointRCAHtml = testpointRCA.replace("\n","</br>")
                testpointFIXSTEP = TESTPOINT[testpoint]["FIXSTEP"]
                testpointFIXSTEP = list2stringAndFormat(testpointFIXSTEP)
                if not testpointFIXSTEP:
                    testpointFIXSTEP = '<font color="#d0d0d0">NA</font>'
                testpointFIXSTEPHtml = testpointFIXSTEP.replace("\n","</br>")
                testpointAutoFixStep = TESTPOINT[testpoint]["AUTOFIXSTEP"]

                if not testpointAutoFixStep:
                    testpointAutoFixStep = '<font color="#d0d0d0">NA</font>'
                else:
                    if ConfigManagerInstance.config["Host"]:
                        reportHash = ConfigManagerInstance.config["__ReportHash__"]
                        reportName = ConfigManagerInstance.config["__ReportName__"]
                        host = ConfigManagerInstance.config["Host"]
                        port = ConfigManagerInstance.config["Port"]
                        user = ConfigManagerInstance.config["User"]
                        password = ConfigManagerInstance.config["Password"]
                        cwd =ConfigManagerInstance.config["__ProjectCWD__"]
                        recovery = {"ProjectDir":cwd,"Host":host,"Port":port,"User":user,"Password":password,"Recovery":",".join(testpointAutoFixStep)}
                        testpointAutoFixStep = """
                        <iframe scrolling="no" src="/www/iframe/growl-genie.html?recovery=%s&reportHash=%s&reportName=%s"></iframe>
                        """%(recovery,reportHash,reportName)

                testpointAutoFixStepHtml = testpointAutoFixStep

                testpointLog = TESTPOINT[testpoint]["LOG"]
                testpointLogHtml = testpointLog
                pattern = re.compile(r"\<.+\>")
                match = pattern.finditer(testpointLog)
                if match:
                    for m in match:
                        className = m.group()
                        testpointLogHtml = testpointLogHtml.replace(className,'<font color="#FFB90F">%s</font>'%className)

                testpointLogHtml = testpointLogHtml.replace("\n", "</br>")
                testpointTimeout = TESTPOINT[testpoint]["TIMEOUT"]
                testpointCost = TESTPOINT[testpoint]["COST"]
                testpointHtml = '<i title="Timeout: %s\nCostTime: %s">%s<i>'%(testpointTimeout,testpointCost,testpoint.strip("{}"))
                attribute = """
                    
                    <tr>
                            <td>
                                <i>%s</i>
                            </td>
                            <td>
                                <i>%s</i>
                            </td>                                                
                            <td>
                                <i>%s</i>
                            </td>
                            <td name="nolog">
                               <i>%s</i>
                            </td>
                            <td name="nolog">
                               <i>%s</i>
                            </td>
                            <td name="nolog">
                               <i>%s</i>
                            </td>
                            <td name="nolog">
                               <i>%s</i>
                            </td>
                            <td style="display:none" name="log">
                               <i>%s</i>
                            </td>
                    </tr>

"""%(testpointHtml,testpointStatusHtml,testpointLevelHtml,testpointImpactHtml,testpointRCAHtml,testpointFIXSTEPHtml,testpointAutoFixStepHtml,testpointLogHtml)
                data += attribute
            data += """
                </table>
            </td>
            </tr>      
        """
        data += """
		</tbody>
	</table>
"""
        data += BUTTON
        # data += HTML_LOG
        data += BODY_AFTER
        data += HTML_AFTER
        reportDir = os.path.dirname(ConfigManagerInstance.config["Report"])
        createDir(reportDir)
        reportPath = ConfigManagerInstance.config["Report"]
        with open(reportPath,"w") as f:
            f.write(data)

