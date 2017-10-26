# -*- coding: utf-8 -*-

MAINCSS = """

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
        border: solid #ccc 3px;
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
.bordered tr:hover {
    background: #FCFDFE;
    }
.bordered td,
.bordered th {
    border-left: 2px solid #ccc;
    border-top: 2px solid #ccc;
    padding: 10px;
    text-align: left;
    }
.bordered th {
    //background-color: #dce9f9;
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
"""


BUTTON ="""
<section class="model-1">
    <div class="checkbox">
        <input type="checkbox"  onclick="checkboxOnclick(this)"/>
        <label></label>
    </div>
</section>"""


BUTTONCSS = """
<style type="text/css">
.checkbox {
  position: relative;
  display: inline-block;
}
.checkbox:after, .checkbox:before {
  font-family: FontAwesome;
  -webkit-font-feature-settings: normal;
     -moz-font-feature-settings: normal;
          font-feature-settings: normal;
  -webkit-font-kerning: auto;
     -moz-font-kerning: auto;
          font-kerning: auto;
  -webkit-font-language-override: normal;
     -moz-font-language-override: normal;
          font-language-override: normal;
  font-stretch: normal;
  font-style: normal;
  font-synthesis: weight style;
  font-variant: normal;
  font-weight: normal;
  text-rendering: auto;
}
.checkbox label {
  width: 75px;
  height: 25px;
  background: #ccc;
  position: relative;
  display: inline-block;
  border-radius: 46px;
  -webkit-transition: 1s;
  transition: 1s;
}
.checkbox label:after {
  content: '';
  position: absolute;
  width: 35px;
  height: 35px;
  border-radius: 100%;
  left: 0;
  top: -5px;
  z-index: 2;
  background: #fff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  -webkit-transition: 1s;
  transition: 1s;
}
.checkbox input {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 5;
  opacity: 0;
  cursor: pointer;
}
.checkbox input:hover + label:after {
  box-shadow: 0 2px 15px 0 rgba(0, 0, 0, 0.2), 0 3px 8px 0 rgba(0, 0, 0, 0.15);
}
.checkbox input:checked + label:after {
  left: 40px;
}

.model-1 .checkbox input:checked + label {
  background: #376ecb;
}
.model-1 .checkbox input:checked + label:after {
  background: #4285F4;
}
</style>
"""
BUTTONJS = """
<script>
function checkboxOnclick(checkbox){

if ( checkbox.checked == true){

//Action for checked
//document.getElementsById("log").style.display="";//显示
var logs = document.getElementsByName("log")
var nologs = document.getElementsByName("nolog")
for(var i=0;i<logs.length;i++)
    {
 logs[i].style.display="";
    }

for(var i=0;i<nologs.length;i++)
    {
 nologs[i].style.display="none";
    }

}else{

var logs = document.getElementsByName("log")
var nologs = document.getElementsByName("nolog")
for(var i=0;i<logs.length;i++)
    {
 logs[i].style.display="none";
    }

for(var i=0;i<nologs.length;i++)
    {
 nologs[i].style.display="";
    }


//Action for not checked
//document.getElementsById("log").style.display="none";//隐藏
}}

</script>
"""




SPINJS = """
<script>
function spin(id) {
var opts = {
  lines: 13 // The number of lines to draw
, length: 28 // The length of each line
, width: 14 // The line thickness
, radius: 42 // The radius of the inner circle
, scale: 1 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: '#000' // #rgb or #rrggbb or array of colors
, opacity: 0.25 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 60 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '50%' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
}
var target = document.getElementById(id)
var spinner = new Spinner(opts).spin(target);
return spinner
}
</script>
"""

HTML_HEAD = """
<head>
<title>TroubleShooting Framework Report</title>
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
<script src="https://code.jquery.com/jquery-3.2.1.min.js" type="text/javascript"></script>
<script type="text/javascript" src="/www/js/spin.min.js" ></script>
<script type="text/javascript">
$(function(){
$('tr.parent').click(function(){   // 获取父行
$(this)
//	.toggleClass("selected")   // 添加/删除高亮
	.siblings('.child_'+this.id).toggle();  // 隐藏/显示所谓的子行
	});
})
</script>
%s
%s
%s
%s
</head>

"""%(MAINCSS,BUTTONCSS,BUTTONJS,SPINJS)

"""
<script src="/jquery/jquery-1.11.1.min.js">
"""


HTML_BEFORE= """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
""".strip()
HTML_AFTER = """
</html>
"""
BODY_AFTER = """
<div id="spin"></div>
</body>
"""


