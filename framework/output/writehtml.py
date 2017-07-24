# -*- coding: utf-8 -*-
from framework.manager import ManagerFactory
from framework.variable.variable import *
from framework.library.library import list2stringAndFormat
import time
class html(object):
    def __init__(self):
        super(html,self).__init__()
        self.caseResult = ManagerFactory().getManager(LAYER.Case).case_record
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

<style type="text/css">
			*{margin: 0;padding: 0;}
			body {
				padding: 40px 100px;
			}
			.demo {
			width: 600px;
			margin: 40px auto;
			font-family: 'trebuchet MS', 'Lucida sans', Arial;
			font-size: 14px;
			color: #444;
			}

			table {
				*border-collapse: collapse; /* IE7 and lower */
				border-spacing: 0;
				width: 100%;
			}
			/*========bordered table========*/
			.bordered {
				border: solid #ccc 1px;
				-moz-border-radius: 6px;
				-webkit-border-radius: 6px;
				border-radius: 6px;
				-webkit-box-shadow: 0 1px 1px #ccc;
				-moz-box-shadow: 0 1px 1px #ccc;
				box-shadow: 0 1px 1px #ccc;
			}

			.bordered tr {
				-o-transition: all 0.1s ease-in-out;
				-webkit-transition: all 0.1s ease-in-out;
				-moz-transition: all 0.1s ease-in-out;
				-ms-transition: all 0.1s ease-in-out;
				transition: all 0.1s ease-in-out;		
			}
			.bordered .highlight,
		//	.bordered tr:hover {
		//		background: #fbf8e9;		
		//	}
			.bordered td, 
			.bordered th {
				border-left: 1px solid #ccc;
				border-top: 1px solid #ccc;
				padding: 10px;
				text-align: left;
			}
			.bordered th {
				background-color: #dce9f9;
				background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));
				background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);
				background-image: -moz-linear-gradient(top, #ebf3fc, #dce9f9);
				background-image: -ms-linear-gradient(top, #ebf3fc, #dce9f9);
				background-image: -o-linear-gradient(top, #ebf3fc, #dce9f9);
				background-image: linear-gradient(top, #ebf3fc, #dce9f9);
				filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0, startColorstr=#ebf3fc, endColorstr=#dce9f9);
				-ms-filter: "progid:DXImageTransform.Microsoft.gradient (GradientType=0, startColorstr=#ebf3fc, endColorstr=#dce9f9)";
				-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
				-moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset;
				box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
				border-top: none;
				text-shadow: 0 1px 0 rgba(255,255,255,.5);
			}
			.bordered td:first-child, 
			.bordered th:first-child {
				border-left: none;
			}
			.bordered th:first-child {
				-moz-border-radius: 6px 0 0 0;
				-webkit-border-radius: 6px 0 0 0;
				border-radius: 6px 0 0 0;
			}
			.bordered th:last-child {
				-moz-border-radius: 0 6px 0 0;
				-webkit-border-radius: 0 6px 0 0;
				border-radius: 0 6px 0 0;
			}
			.bordered tr:last-child td:first-child {
				-moz-border-radius: 0 0 0 6px;
				-webkit-border-radius: 0 0 0 6px;
				border-radius: 0 0 0 6px;
			}
			.bordered tr:last-child td:last-child {
				-moz-border-radius: 0 0 6px 0;
				-webkit-border-radius: 0 0 6px 0;
				border-radius: 0 0 6px 0;
			}
			/*----------------------*/
			.zebra td, 
			.zebra th {
				padding: 10px;
				border-bottom: 1px solid #f2f2f2;
			}
			.zebra .alternate,
			.zebra tbody tr:nth-child(even) {
				background: #f5f5f5;
				-webkit-box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
				-moz-box-shadow:0 1px 0 rgba(255,255,255,.8) inset;
				box-shadow: 0 1px 0 rgba(255,255,255,.8) inset;
			}
			.zebra th {
				text-align: left;
				text-shadow: 0 1px 0 rgba(255,255,255,.5);
				border-bottom: 1px solid #ccc;
				background-color: #eee;
				background-image: -webkit-gradient(linear, left top, left bottom, from(#f5f5f5), to(#eee));
				background-image: -webkit-linear-gradient(top, #f5f5f5, #eee);
				background-image: -moz-linear-gradient(top, #f5f5f5, #eee);
				background-image: -ms-linear-gradient(top, #f5f5f5, #eee);
				background-image: -o-linear-gradient(top, #f5f5f5, #eee);
				background-image: linear-gradient(top, #f5f5f5, #eee);
				filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0, startColorstr=#f5f5f5, endColorstr=#eeeeee);
				-ms-filter: "progid:DXImageTransform.Microsoft.gradient (GradientType=0, startColorstr=#f5f5f5, endColorstr=#eeeeee)";
			}
			.zebra th:first-child {
				-moz-border-radius: 6px 0 0 0;
				-webkit-border-radius: 6px 0 0 0;
				border-radius: 6px 0 0 0;
			}
			.zebra th:last-child {
				-moz-border-radius: 0 6px 0 0;
				-webkit-border-radius: 0 6px 0 0;
				border-radius: 0 6px 0 0;
			}
			.zebra tfoot td {
				border-bottom: 0;
				border-top: 1px solid #fff;
				background-color: #f1f1f1;
			}
			.zebra tfoot td:first-child {
				-moz-border-radius: 0 0 0 6px;
				-webkit-border-radius: 0 0 0 6px;
				border-radius: 0 0 0 6px;
			}
			.zebra tfoot td:last-child {
				-moz-border-radius: 0 0 6px 0;
				-webkit-border-radius: 0 0 6px 0;
				border-radius: 0 0 6px 0;
			}
</style>



</head>
"""
        data +="""
<body>
<h1 align="center">3GPP Corba FM Sniffer Report</h1>
<p><i>%s</i></p>
	<table width="100%%" border="1" class="bordered">
		<thead>
			<tr bgcolor="#1E90FF"><th width="15%%">CaseName</th><th width="5%%" >Status</th><th width="80%%">Attribute</th></tr>
		</thead>
		<tbody>
		
"""%self.currenttime
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

#                 attribute_pass = """
#                     <tr class="child_row_0%s">
#                         <td>%s</td>
#                         <td>%s</td>
#                         <td>%s</td>
#                         <td>%s</td>
#                         <td>%s</td>
#                         <td>%s</td>
#                     </tr>
# """%(i,testpointHtml,testpointStatusHtml,testpointLevel,testpointImpactHtml,testpointRCAHtml,testpointFIXSTEPHtml)
#                 data += attribute_pass if testpointStatus else attribute_fail
                data += attribute
            data += """
                </table>
            </td>
            </tr>      
        """
        data += """
		</tbody>
	</table>
</body>
</html>
"""
        with open("report.html","w") as f:
            f.write(data)
