===============================================================================
`TroubleShooting Framework   <https://github.com/gaoxiaofeng/troubleShooting>`_
===============================================================================


*************
Introduction:
*************

TroubleShooting Framework is a generic open source test-analysis-fix automation framework for troubleshooting.
TroubleShooting Framework is operating system and application independent. The core framework is implemented using Python, supports Python 2.6 and Python 2.7, and run also on Jython,IronPython and Pypy. 
TroubleShooting Framework project is hosted on GitHub where you can find source code, an issue tracker, and some further documentation. 

.. image:: https://img.shields.io/pypi/v/troubleshooting-framework.svg?label=version
   :target: https://pypi.python.org/pypi/troubleshooting-framework
   :alt: Latest version

.. image:: https://img.shields.io/pypi/l/troubleshooting-framework.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
   :alt: License

*************
Installation
*************


If you already have `Python <http://python.org>`_  with `PIP <https://pypi.python.org/pypi/pip/>`_ installed,you can simply run::

    pip install troubleshooting-framework

Alternatively you can get TroubleShooting Framework source code by downloading the source
distribution from PyPI and extracting it, or by cloning the project repository
from GitHub. After that you can install the framework with::

    python setup.py install

  

*************************
Development:
*************************

1. Create a project
===================

you can simply run::

    pytsmgr --operation=startProject --project=<MyProject> --directory=<ProjectDirectory>


2. Add a keyword
==================
new a <keywordName>.py file in <ProjectDirectory>/<MyProject>/keywords folder:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
from troubleshooting.framework.template._BaseKeyword import _BaseKeyword

class keywordName(_BaseKeyword):
    def __init__(self):
        super(,self).__init__()
    def getExample(self):
        return "example"

3. Add a testpoint 
==================

new a <testPointName>.py file in <ProjectDirectory>/<MyProject>/testpoint folder:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
from framework.variable.variable import STATUS,LEVEL

from troubleshooting.framework.template._BaseTestPoint import _BaseTestPoint

class testPointName(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVLE.CRITICAL

    def _checkpoint(self):
        result = self.getExample()

        if result is "example":
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
            self.IMPACT.append("system is not working")
            self.RCA.append("Bad luck")
            self.FIXSTEP.append("bathing")
            self.FIXSTEP.append("say hello god!")

Note:   **self.status** is mandatory, it's enum type , value is **STATUS.PASS** or **STATUS.FAIL**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note:   **self.level** is option, it's enum type , value is **LEVLE.CRITICAL** or **LEVLE.NOCRITICAL** , default is **LEVLE.NOCRITICAL**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note:   **self.IMPACT** , **self.RCA** and **self.FIXSTEP** is option, it's list type.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4. Add a case
==============

new a <caseName>.py file in <ProjectDirectory>/<MyProject>/case folder:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
from troubleshooting.framework.template._BaseCase import _BaseCase

class caseName(_BaseCase):
    """
    To Check linux disk usage.
    """

    def __init__(self):
        super(caseName,self).__init__()

        self.passCondition = "{testPointName} is True"

        self.tags = "example goodcase"

Note:   **self.passCondition** is mandatory, it's condition of case pass.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note:   **self.tags** is option, it's a string and fragment by space.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

******
Usage:
******

Switch folder to  <ProjectDirectory>/<MyProject>/ , you can simple run::
==============================================================================

    pyts --host=<IP> 

Options:
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  --host=HOST          host for remote connection
  --port=PORT          port for remote connection ,defaut port is 22
  --user=USER          user for remote connection , default user is root
  --password=PASSWORD  password for remote connection , default password is
                       arthur
  --name=NAME          select the case to run by name
  --include=INCLUDE    select cases to run by tag, Tags can also be combined
                       together with  `AND` and `OR` .     Example:
                       --include=coolANDhot
  --exclude=EXCLUDE    select cases not to run by tag. Tags can also be
                       combined together with  `AND` and `OR` .     Example:
                       --include=coolORhot
  --report=REPORT      HTML report file, default is report.html


********
Example:
********

you can simple run::

    pyts --host=192.168.10.10  --include=exampleANDsmoke --exclude=NoRunORdisable

if you are working on Windows, you can use pyts.bat::

    pyts.bat --host=192.168.10.10  --include=exampleANDsmoke --exclude=NoRunORdisable


*********************
Support And Contact:
*********************

zeus.gao@foxmail.com

*******
License
*******


TroubleShooting Framework is open source software provided under the Apache License 2.0. TroubleShooting Framework documentation and other similar content use the Creative Commons Attribution 3.0 Unported license. Most libraries and tools in the ecosystem are also open source, but they may use different licenses.
^