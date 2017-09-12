from optparse import  OptionParser
from troubleshooting.framework.version.version import VERSION
import sys,os
class BaseCommand(object):
    """
    this is command
    """
    def __init__(self):
        super(BaseCommand,self).__init__()
        self.opt = None
        self.successor = None
    def handle(self,*args,**kwargs):
        # raise Exception("subclass of BaseCommand must provide a handle() method")
        if self.successor:
            self.successor.handle(*args,**kwargs)
    def create_parser(self):
        return  OptionParser(VERSION)
    def help(self,opt):
        # opt = OptionParser()
        print opt.print_help()
    def execute(self,*args):
        raise Exception("subclass of BaseCommand must provide a execute() method")
    def get_version(self):
        return  VERSION

    def cut_args(self,*args):
        argv = [sys.argv[0]]
        for _argv in sys.argv[1:]:
            for condition in args:
                if condition in _argv:
                    argv.append(_argv)
        return argv
    def mkdir(self,path):
        if os.path.exists(path):
            raise Exception("File already Exist %s"%path)
        os.makedirs(path)
    def create_file(self,path,content=""):
        if os.path.exists(path):
            raise Exception("File alredady Exist %s"%path)
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            self.mkdir(directory)
        with open(path,"wb") as f:
            f.write(content)







