import sys,os,time
from subprocess import Popen, PIPE
from framework.variable.variable import *
# import  threading
import re
from framework.log.logger import logger
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
            # self.logger.error(message)
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
            # message = '\n'.join([command_str,err])
            # self.logger.error(message)
            raise Exception(err)
        return stdout

    def shell_script(self,PATH,scriptname,*args,**kw):

        simulator_path = os.path.join(PATH,scriptname)
        self._check_simulator_exist(simulator_path)
        command =['sh',scriptname] + list(args)
        command_str = ' '.join(command)
        shell =Popen(command ,cwd =PATH,stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = shell.communicate()

        if  err:
            # message = '\n'.join([command_str,err])
            # self.logger.error(message)
            raise Exception(err)
        return stdout

    def shell_command(self,command):
        shell =Popen([command] ,stdout=PIPE, stdin=PIPE,stderr = PIPE,shell = True)
        stdout, err = shell.communicate()
        if err:
            # message = '\n'.join([command,err])
            # self.logger.error(message)
            raise Exception(err)
        return stdout
class _GetchUnix(object):
    def __init__(self):
        super(_GetchUnix, self).__init__()
        import tty,sys,termios
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
##class _GetchWindows(object):
##    def __init__(self):
##        super(_GetchWindows, self).__init__()
##        import msvcrt
##    def __call__(self):
##        import msvcrt
##        return  msvcrt.getch()
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

# class ProgressDialog(threading.Thread):
#     def __init__(self,total):
#         super(ProgressDialog,self).__init__()
#         self._total = total
#         self._done = 0
#         self._ratio = 0
#         self._RUN = True
#         self.printf =
#     def set(self):
#         return self._done
#     def set(self,num):
#         if isinstance(num,int):
#             self._done = num
#             self._ratio = float(self._done)/float(self._total)
#         else:
#             print "Progress is not int",num
#     def run(self):
#         while self._RUN:
#             done = "#"*int(self._ratio*PROGREES_LENHTH)
#             undone = " " *(PROGREES_LENHTH - int(self._ratio*PROGREES_LENHTH))
#             sys.stdout.write("\rProgress:[%s%s]  %s/%s"%(done,undone,self._done,self._total))
#             sys.stdout.flush()
#             if self._done == self._total:
#                 break
#             time.sleep(0.01)
#         if self._RUN:
#             sys.stdout.write( "\tSuccess.\n")
#     def stop(self):
#         self._RUN = False
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



if __name__ == "__main__":
    command = ExecuteCommond()
    stdout = command.jar_command("/opt/oss/NSN-nbi3gc/simulator","AlarmIRPSim.jar","-o=get_alarm_list")
    print stdout

