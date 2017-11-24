# -*- coding: utf-8 -*-
import sys,os,time
from subprocess import Popen, PIPE
import hashlib
import re
from troubleshooting.framework.log.logger import logger
Logger = logger()


def singleton(cls,*args,**kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton

def parseRule(rule):
    checkPointList = []
    pattern = re.compile(r".*?(\{.+?\}).*",re.S)
    while 1:
        match = pattern.match(rule)
        if match:
            checkPoint =  match.group(1)
            checkPointList.append(checkPoint)
            rule = rule.replace(checkPoint,"")
        else:
            break
    return checkPointList



@singleton
class ExecuteCommond(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.logger = logger()

    def _check_simulator_exist(self,simulator_path):
        if not os.path.isfile(simulator_path):
            err = "Simulator %s is not Found"%simulator_path
            self.logger.error(message)
            # return NOEXIST
            raise Exception(err)
    def jar_command(self,PATH,simulator,*args):

        simulator_path = os.path.join(PATH,simulator)
        self._check_simulator_exist(simulator_path)

        command =['java','-jar',simulator] + list(args)
        command_str = ' '.join(command)
        java =Popen(command,cwd =PATH,stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = java.communicate()
        if err:
            # message = '\n'.join([command_str,err])
            # self.logger.error(message)
            raise Exception(err)
        return stdout
    def java_command(self,*args):

        command =['java'] + list(args)
        command_str = ' '.join(command)
        java =Popen(command,cwd ="/home",stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = java.communicate()
        if err:
            raise Exception(err)
        return stdout

    def shell_script(self,PATH,scriptname,*args,**kw):

        simulator_path = os.path.join(PATH,scriptname)
        self._check_simulator_exist(simulator_path)
        command =['sh',scriptname] + list(args)
        shell =Popen(command ,cwd =PATH,stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = shell.communicate()

        if  err:
            raise Exception(err)
        return stdout

    def shell_command(self,command,checkerr=False):
        shell =Popen([command] ,stdout=PIPE, stdin=PIPE,stderr = PIPE,shell = True)
        stdout, err = shell.communicate()
        if checkerr and err:
            raise Exception(err)
        return stdout
class _GetchUnix(object):
    def __init__(self):
        super(_GetchUnix, self).__init__()
    def __call__(self):
        import tty, sys, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
        return ch

class _GetchWindows(object):
    def __init__(self):
        super(_GetchWindows, self).__init__()
        import msvcrt
    def __call__(self):
        return raw_input()


class Getch(object):
    def __init__(self):
        super(Getch,self).__init__()
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self):
        return  self.impl()

def RemoveDuplicates(list):
    finalList = []
    for elem in list:
        if elem not in finalList:
            finalList.append(elem)
    return finalList

def conversion(x):
    # to bytes
    pattern = re.compile("(\d+).*",re.I)
    match = pattern.match(x)
    if match:
        y = int(match.group(1))
    x = x.lower()
    if "kb" in x:
        y = y * 1024
    elif "mb" in x:
        y = y * 1024 * 1024
    elif "gb" in x:
        y = y * 1024 * 1024 * 1024
    elif  "tb" in x:
        y = y * 1024 * 1024 * 1024 * 1024
    else :
        pass
    return  y
def list2stringAndFormat(List):
    result = []
    for i,line in enumerate(List):
        i += 1
        line = "%s. %s"%(i,line)
        result.append(line)
    return "\n".join(result)

def dict_value_contain_content(dict,content):
    for key in dict:
        if dict[key] == content:
            return  True
    return  False

def  getFileMd5(filename):
    if not os.path.isfile(filename):
        raise Exception("failed to get file md5, reason :%s is not a file"%filename)
    myhash = hashlib.md5()
    with open(filename,"rb") as f:
        content = f.read()
        myhash.update(content)
    return  myhash.hexdigest()

def convertTime(Timestr):
    Time = 0
    pattern_hours = re.compile(".*?(\d+)\s*h")
    match = pattern_hours.match(Timestr)
    if match:
        _hours = match.group(1)
        try:
            _hours_int = int(_hours)
        except:
            _hours_int = 0
        Time += 3600 * _hours_int

    pattern_minutes = re.compile(".*?(\d+)\s*m")
    match = pattern_minutes.match(Timestr)
    if match:
        _minutes = match.group(1)
        try:
            _minutes_int = int(_minutes)
        except:
            _minutes_int = 0
        Time += 60 * _minutes_int

    pattern_secs = re.compile(".*?(\d+)\s*s")
    match = pattern_secs.match(Timestr)
    if match:
        _secs = match.group(1)
        try:
            _secs_int = int(_secs)
        except:
            _secs_int = 0
        Time += _secs_int

    return Time
def getRandomString(lengh):
    import random
    source = "abcdefghijklmnopqlstuvwxyz"
    result = []
    for i in range(lengh):
        result.append(random.choice(source))
    return "".join(result)

def isSublist(parentlist,sublist):
    for elem in sublist:
        if elem not in parentlist:
            return False
    return True
def compareList(left,right):
    diff = []
    for elem in right:
        if elem not in left:
            diff.append(elem)
    return diff
def parseRecoveryArgs(argsString):
    import re
    recoverStepsParsed = []
    recoverSteps = argsString.split(",")
    pattern = re.compile(r"([\d\w_]+)\(*([^\(\)]*)\)*", re.I)
    for step in recoverSteps:
        match = pattern.match(step)
        if match:
            method = match.group(1)
            args = match.group(2)
            recoverStepsParsed.append({"method":method,"args": args})
    return recoverStepsParsed



if __name__ == "__main__":
    # print convertTime("1 h 1 mins 1sec")
    # print parseRecoveryArgs("touchFile(/home/testfile_  haha.txt)")
    pass
