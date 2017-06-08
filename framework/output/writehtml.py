# -*- coding: utf-8 -*-
from framework.manager import CaseManagerInstance
from framework.variable.variable import *
from framework.library.library import list2stringAndFormat
import time
class html(object):
    def __init__(self):
        super(html,self).__init__()
        self.caseResult = CaseManagerInstance.case_record
        self.currenttime = time.strftime("%Y-%m-%d %X %Z",time.localtime())
    def write(self):
        data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>3GPP Corba FM Sniffer Report</title>
<style>
table{ border:1;border-collapse:collapse;}
td{ font:normal 12px/17px Arial;padding:2px;}
th{ font:bold 12px/17px Arial;text-align:left;padding:4px;border-bottom:1px solid #333;}
tr{ font:bold 12px/17px Arial;text-align:left;padding:4px;border-bottom:1px solid #333;}
//.parent{ background:#FFF38F;cursor:pointer;}  /* 偶数行样式*/
.odd{ background:#FFFFEE;}  /* 奇数行样式*/
.selected{ background:#FF6500;color:#fff;}
</style>
<!--   引入jQuery -->
<script src="http://www.codefans.net/ajaxjs/jquery1.3.2.js" type="text/javascript"></script>
<script type="text/javascript">
$(function(){
$('tr.parent').click(function(){   // 获取父行
$(this)
//	.toggleClass("selected")   // 添加/删除高亮
	.siblings('.child_'+this.id).toggle();  // 隐藏/显示所谓的子行
	});
})
</script>

</head>
"""
        data +="""
<body>
<h1 align="center">3GPP Corba FM Sniffer Report</h1>
<p><i>%s</i></p>
	<table width="100%%" border="1" >
		<thead>
			<tr><th width="15%%">CaseName</th><th width="5%%" >Status</th><th width="80%%">Attribute</th></tr>
		</thead>
		<tbody>
"""%self.currenttime
        for i,caseName in enumerate(self.caseResult):
            i += 1
            caseStatus = self.caseResult[caseName]["STATUS"]
            caseStatusHtml = '<td colspan="1" bgcolor="#00FF00">%s</td>'%STATUS.PASS if caseStatus else '<td colspan="1" bgcolor="#FF0000">%s</td>'%STATUS.FAIL
            DESCRIPTION = self.caseResult[caseName]["DESCRIPTION"]
            REFERENCE = self.caseResult[caseName]["REFERENCE"]
            REFERENCEHtml = '<a href="%s">reference document</>'%REFERENCE if REFERENCE else REFERENCE
            TESTPOINT = self.caseResult[caseName]["TESTPOINT"]
            parent_pass = """
            <tr  bgcolor="#00FF00" class="parent" id="row_0%s"><td colspan="1">%s</td>%s<td colspan="1"></td></tr>"""%(i,caseName,caseStatusHtml,)
            parent_fail = """
            <tr  bgcolor="#FF0000" class="parent" id="row_0%s"><td colspan="1">%s</td>%s<td colspan="1"></td></tr>"""%(i,caseName,caseStatusHtml,)
            data += parent_pass if caseStatus else parent_fail
            data += """
			<tr class="child_row_0%s"><td>Description</td><td></td><td>%s</td></tr>
			<tr class="child_row_0%s"><td>Reference</td><td></td><td>%s</td></tr>
"""%(i,DESCRIPTION,i,REFERENCEHtml)
            data += """<tr class="child_row_0%s">
            <td><font color="blue"><b>TestPoint</b></font></td>
            <td><font color="blue"><b>Status</b></font></td>
            <td><font color="blue"><b>Attribute</b></font></td>
            </tr>"""%i
            for testpoint in TESTPOINT:
                testpointStatus = TESTPOINT[testpoint]["STATUS"]
                testpointStatusHtml = '<font color="green"><b><i>%s</i></b></font>' % STATUS.PASS.lower() if testpointStatus else '<font color="red"><b><i>%s</i></b></font>' % STATUS.FAIL.lower()
                testpointImpact = TESTPOINT[testpoint]["IMPACT"]
                testpointImpact = list2stringAndFormat(testpointImpact)
                testpointLevel =  TESTPOINT[testpoint]["LEVEL"]
                testpointLevel = "<i>%s</i>"%testpointLevel
                testpointDescribe = TESTPOINT[testpoint]["DESCRIBE"]
                testpointRCA = TESTPOINT[testpoint]["RCA"]
                testpointRCA = list2stringAndFormat(testpointRCA)
                testpointFIXSTEP = TESTPOINT[testpoint]["FIXSTEP"]
                testpointFIXSTEP = list2stringAndFormat(testpointFIXSTEP)
                testpointHtml = "<i>%s<i>"%testpoint.strip("{}")
                attribute_fail = """
            <tr class="child_row_0%s">
            <td>%s</td>
            <td>%s</td>
            <td>
                <table border="1"  width="100%%" style="margin:20px">
                    <tr>
                            <th width="10%%">
                                <b>Level</b>
                            </th>
                            <th width="30%%">
                               <b>Impact</b>
                            </th>
                            <th width="30%%">
                               <b>Root Cause</b>
                            </th>
                            <th width="30%%">
                               <b>Fix Method</b>
                            </th>
                    </tr>
                    <tr>
                            <td>
                                <b>%s</b>
                            </td>
                            <td>
                               <b>%s</b>
                            </td>
                            <td>
                               <b>%s</b>
                            </td>
                            <td>
                               <b>%s</b>
                            </td>
                    </tr>
                </table>
            </td>
            </tr>
"""%(i,testpointHtml,testpointStatusHtml,testpointLevel,testpointImpact,testpointRCA,testpointFIXSTEP)
                attribute_pass = """
            <tr class="child_row_0%s">
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            </tr>
"""%(i,testpointHtml,testpointStatusHtml,testpointLevel,)
                data += attribute_pass if testpointStatus else attribute_fail
        data += """
		</tbody>
	</table>
</body>
</html>
"""
        with open("report.html","w") as f:
            f.write(data)
