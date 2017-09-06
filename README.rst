===============================================================================
`TroubleShooting Framework   <https://github.com/gaoxiaofeng/troubleShooting>`_
===============================================================================


************
Introduction
************

TroubleShooting Framework is a generic open source test-analysis-fix automation framework for troubleshooting.
TroubleShooting Framework is operating system and application independent. The core framework is implemented using Python, supports Python 2.6 and Python 2.7, and run also on Jython,IronPython and Pypy. 
TroubleShooting Framework project is hosted on GitHub where you can find source code, an issue tracker, and some further documentation. 



*****
Usage
*****
Usage: runner.py [options]

Options:
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  --host=HOST          host for remote connection
  --port=PORT          port for remote connection ,defaut port is 22
  --user=USER          user for remote connection , default user is root
  --password=PASSWORD  password for remote connection , default password is
                       arthur
  --sync=SYNC          yes/no,default is yes
  --console=CONSOLE    set console to on/off,default is on
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
python runner.py --host=192.168.10.10  --include=exampleANDsmoke --exclude=NoRunORdisable

**********
Contact me
**********
zeus.gao@foxmail.com

