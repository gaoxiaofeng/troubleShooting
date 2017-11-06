from troubleshooting.framework.management.BaseCommand import  BaseCommand
from os.path import join,isdir,dirname
class command(BaseCommand):
    def __init__(self):
        super(command,self).__init__()
    def handle(self,*args,**kwargs):
        try:
            self.add_argument(*args,**kwargs)
            super(command, self).handle(*args, **kwargs)
        except Exception,e:
            print e

    def add_argument(self,opt,*args,**kwargs):
        opt = self.create_parser()
        opt.add_option("--project",dest="project",help="project name for create a project")
        opt.add_option("--directory",dest="directory",help="project directory for create a project")
        options,args = opt.parse_args(self.cut_args("--project","--directory","-h","--help"))
        project = options.project
        directory = options.directory
        if project and directory:
            if not isdir(directory):
                raise Exception("Directory is not exist, directory is %s"%directory)
            self.execute(project=project,directory=directory)
        else:
            if not project:
                e = """
You must provide a project name:
Options:
  --project=PROJECT     project name for create a project
                """.strip()
                raise Exception(e)
            if not directory:
                e = """
You must provide a project directory:
Options:
  --directory=DERECTORY     project directory for create a project
                """
                raise Exception(e)
    def execute(self,*args,**kwargs):
        project = kwargs.pop("project")
        directory = kwargs.pop("directory")
# """
# -- case
#    -- __init__.py
# -- testpoint
#    -- __init__.py
# -- keywords
#    -- __init__.py
# -- config
#    -- __init__.py
#    -- variable.py
# """

        project_path = join(directory,project)
        self.mkdir( project_path)
        initFiles = [join(project_path,foler,"__init__.py") for foler in ("case","testpoint","keywords","config","lib","recovery")]
        for initFile in initFiles:
            self.create_file(initFile)
        variableFile = join(project_path,"config","variable.py")
        self.create_file(variableFile)
        print "create successfully."


