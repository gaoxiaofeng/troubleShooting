# -*- coding: utf-8 -*-
from framework.manager import ManagerFactory
from framework.variable.variable import *
from framework.libraries.library import list2stringAndFormat
import time
from htmltemplate import *
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
<body>
<h1 align="center">3GPP Corba FM Sniffer Report</h1>
<p><i>%s</i></p>
	<table width="100%%" border="1" class="bordered">
		<thead>
			<tr bgcolor="#1E90FF"><th width="15%%">CaseName</th><th width="5%%" >Status</th><th width="80%%">Attribute</th></tr>
		</thead>
		<tbody>
"""%(self.currenttime,)
        for i,caseName in enumerate(self.caseResult):
            i += 1
            caseStatus = self.caseResult[caseName]["STATUS"]
            DESCRIPTION = self.caseResult[caseName]["DESCRIPTION"]
            REFERENCE = self.caseResult[caseName]["REFERENCE"]
            REFERENCEHtml = '<a href="%s">reference document</>'%REFERENCE if REFERENCE else '<font color="#d0d0d0">NA</font>'
            TESTPOINT = self.caseResult[caseName]["TESTPOINT"]
            parent_pass = """
            <tr  bgcolor="#90EE90" class="parent" id="row_0%s"><td colspan="1">%s</td><td>PASS</td><td colspan="1"></td></tr>"""%(i,caseName,)
            parent_fail = """
            <tr  bgcolor="#FF3030" class="parent" id="row_0%s"><td colspan="1">%s</td><td>FAIL</td><td colspan="1"></td></tr>"""%(i,caseName,)
            parent_warn = """
            <tr  bgcolor="#FF7F00" class="parent" id="row_0%s"><td colspan="1">%s</td><td>WARN</td><td colspan="1"></td></tr>"""%(i,caseName,)
            if caseStatus:
                data += parent_pass
            else:
                _level = self.caseResult[caseName]["FAILURELEVEL"]
                if _level is LEVEL.CRITICAL:
                    data += parent_fail
                else:
                    data += parent_warn

            data += """
            <tr class="child_row_0%s" style="display:none"><td>Description</td><td></td><td>%s</td></tr>
            <tr class="child_row_0%s" style="display:none"><td>Reference</td><td></td><td>%s</td></tr>
"""%(i,DESCRIPTION,i,REFERENCEHtml)
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
                            <th width="15%%">
                               <b>Impact</b>
                            </th>
                            <th width="35%%">
                               <b>Root Cause</b>
                            </th>
                            <th width="35%%">
                               <b>Fix Method</b>
                            </th>
                    </tr>            
                    """
            for testpoint in TESTPOINT:
                testpointStatus = TESTPOINT[testpoint]["STATUS"]
                testpointStatusHtml = '<font color="green"><b><i>%s</i></b></font>' % STATUS.PASS.lower() if testpointStatus else '<font color="red"><b><i>%s</i></b></font>' % STATUS.FAIL.lower()
                testpointImpact = TESTPOINT[testpoint]["IMPACT"]
                testpointImpact = list2stringAndFormat(testpointImpact)
                if not testpointImpact:
                    testpointImpact = '<font color="#d0d0d0">NA</font>'
                testpointImpactHtml = testpointImpact.replace("\n","</br>")
                testpointLevel =  TESTPOINT[testpoint]["LEVEL"]
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
                testpointHtml = "<i>%s<i>"%testpoint.strip("{}")
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
                            <td>
                               <i>%s</i>
                            </td>
                            <td>
                               <i>%s</i>
                            </td>
                            <td>
                               <i>%s</i>
                            </td>
                    </tr>

"""%(testpointHtml,testpointStatusHtml,testpointLevel,testpointImpactHtml,testpointRCAHtml,testpointFIXSTEPHtml)

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
        from framework.output.Print import CONSOLE
        with open("troubleshooting.log", "r") as f:
            _lines = f.readlines()
            lines = []
            for line in _lines:
                if "^^^^" in line:
                    continue
                if line.startswith("|"):
                    line = line[1:]
                if "|logger" in line:
                    line = line.replace("|logger","")
                lines.append(line)


        content = "".join(lines)
        content = content.replace("\n", "</br>")
        content = content.replace("|","&nbsp;&nbsp;&nbsp;&nbsp;")
        HTML_LOG = '<div style="display:none" id="log" style="font-size:12px"><i>' + content + '</i></div>'
        data += BUTTON
        data += HTML_LOG
        data += BODY_AFTER
        data += HTML_AFTER
        with open("report.html","w") as f:
            f.write(data)