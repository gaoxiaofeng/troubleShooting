import sys,os,time
from log.logger import logger
from subprocess import Popen, PIPE
from variable.variable import *
import re
from log.logger import logger
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
            message = "Simulator %s is not Found"%simulator_path
            self.logger.error(message)
            return NOEXIST
    def jar_command(self,PATH,simulator,*args):

        simulator_path = os.path.join(PATH,simulator)
        if self._check_simulator_exist(simulator_path) == NOEXIST:
            return None

        command =['java','-jar',simulator] + list(args)
        command_str = ' '.join(command)
        java =Popen(command,cwd =PATH,stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = java.communicate()
        if err:
            message = '\n'.join([command_str,err])
            self.logger.error(message)
        return stdout
    def java_command(self,*args):

        command =['java'] + list(args)
        command_str = ' '.join(command)
        java =Popen(command,cwd ="/home",stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = java.communicate()
        if err:
            message = '\n'.join([command_str,err])
            self.logger.error(message)
        return stdout

    def shell_script(self,PATH,scriptname,*args,**kw):

        simulator_path = os.path.join(PATH,scriptname)
        if self._check_simulator_exist(simulator_path) == NOEXIST:
            return None

        command =['sh',scriptname] + list(args)
        command_str = ' '.join(command)
        shell =Popen(command ,cwd =PATH,stdout=PIPE, stdin=PIPE,stderr = PIPE)
        stdout, err = shell.communicate()

        if  err:
            message = '\n'.join([command_str,err])
            self.logger.error(message)
        return stdout

    def shell_command(self,command):
        shell =Popen([command] ,stdout=PIPE, stdin=PIPE,stderr = PIPE,shell = True)
        stdout, err = shell.communicate()
        if err:
            message = '\n'.join([command,err])
            self.logger.error(message)
        return stdout



if __name__ == "__main__":
    command = ExecuteCommond()
    stdout = command.jar_command("/opt/oss/NSN-nbi3gc/simulator","AlarmIRPSim.jar","-o=get_alarm_list")
    print stdout

