import webbrowser
class Browser(object):
    def __init__(self):
        super(Browser,self).__init__()
    def openLocalReport(self,report):
        webbrowser.open(report,new = 1)
