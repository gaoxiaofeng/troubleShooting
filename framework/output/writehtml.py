# -*- coding: utf-8 -*-
from framework.manager import CaseManagerInstance
from framework.variable.variable import *
class html(object):
    def __init__(self):
        super(html,self).__init__()
        self.caseResult = CaseManagerInstance.case_record
    def write(self):
        data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>3GPP Corba FM Sniffer Report</title>
<style>
table{ border:0;border-collapse:collapse;}
td{ font:normal 12px/17px Arial;padding:2px;width:100px;}
th{ font:bold 12px/17px Arial;text-align:left;padding:4px;border-bottom:1px solid #333;width:100px;}
.parent{ background:#FFF38F;cursor:pointer;}  /* 偶数行样式*/
.odd{ background:#FFFFEE;}  /* 奇数行样式*/
.selected{ background:#FF6500;color:#fff;}
</style>
<!--   引入jQuery -->
<script src="http://www.codefans.net/ajaxjs/jquery1.3.2.js" type="text/javascript"></script>
<script type="text/javascript">
$(function(){
$('tr.parent').click(function(){   // 获取所谓的父行
$(this)
	.toggleClass("selected")   // 添加/删除高亮
	.siblings('.child_'+this.id).toggle();  // 隐藏/显示所谓的子行
	});
})
</script>
</head>
"""
        data +="""
<body>
	<table>
		<thead>
			<tr><th>CaseName</th><th>Status</th></tr>
		</thead>
		<tbody>
"""
        for i,caseName in enumerate(self.caseResult):
            i += 1
            caseStatus = self.caseResult[caseName]["STATUS"]
            caseStatus = STATUS.PASS if caseStatus else STATUS.FAIL
            DESCRIPTION = self.caseResult[caseName]["DESCRIPTION"]
            REFERENCE = self.caseResult[caseName]["REFERENCE"]
            TESTPOINT = self.caseResult[caseName]["TESTPOINT"]
            data += """
			<tr class="parent" id="row_0%s"><td colspan="1">%s</td><td colspan="1">%s</td></tr>
			<tr class="child_row_0%s"><td>DESCRIPTION</td><td>%s</td></tr>
			<tr class="child_row_0%s"><td>REFERENCE</td><td>%s</td></tr>

"""%(i,caseName,caseStatus,i,DESCRIPTION,i,REFERENCE)
            for testpoint in TESTPOINT:
                testpointStatus = TESTPOINT[testpoint]["STATUS"]
                testpointImpact = TESTPOINT[testpoint]["IMPACT"]
                testpointLevel =  TESTPOINT[testpoint]["LEVEL"]
                testpointDescribe = TESTPOINT[testpoint]["DESCRIBE"]
                data += """
            <tr class="child_row_0%s"><td>%s</td><td>%s</td><td>%s</td></tr>
"""%(i,testpoint,testpointStatus,testpointLevel)
        data += """
		</tbody>
	</table>
</body>
</html>
"""
        with open("report.html","w") as f:
            f.write(data)

"""
			<tr class="parent" id="row_01"><td colspan="3">前台设计组</td></tr>
			<tr class="child_row_01"><td>张山</td><td>男</td><td>浙江宁波</td></tr>
			<tr class="child_row_01"><td>李四</td><td>女</td><td>浙江杭州</td></tr>
			<tr class="parent" id="row_02"><td colspan="3">前台开发组</td></tr>
			<tr class="child_row_02"><td>王五</td><td>男</td><td>湖南长沙</td></tr>
"""