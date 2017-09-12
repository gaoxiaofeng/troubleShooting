from troubleshooting.framework.management.commands import main,startProject
class client(object):
    def __init__(self):
        super(client,self).__init__()
    def handle(self,*args):
        mainInstance = main.command()
        mainInstance.handle(*args)