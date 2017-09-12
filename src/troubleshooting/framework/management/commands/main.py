from troubleshooting.framework.management.BaseCommand import  BaseCommand
from troubleshooting.framework.management.commands import startProject
import os,sys
class command(BaseCommand):
    def __init__(self):
        super(command,self).__init__()
    def handle(self,*args,**kwargs):
        try:
            self.add_argument(*args,**kwargs)
            super(command, self).handle(*args, **kwargs)
        except Exception,e:
            print e

    def add_argument(self,*args,**kwargs):
        opt = self.create_parser()
        opt.add_option("--operation", dest="operation", help="operation for management")
        options,args = opt.parse_args(self.cut_args("--operation","-h","--help"))
        operation = options.operation
        if operation and operation.lower() == "startproject":
            self.successor = startProject.command()
        else:
            e = """
You must provide a operation:
Options:
  --operation=OPERATION
      startProject       init a new project
            """.strip()
            raise Exception(e)
    def execute(self,*args,**kwargs):
        pass


