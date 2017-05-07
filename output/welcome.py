# -*- coding: utf-8 -*-
from output import OutPut
from library.library import  singleton
@singleton
class welcome(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.printf = OutPut().printf
        self._welcome()
    def _welcome(self):
        graph = """
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
        """
#         graph = """
# ████████╗ ██████╗ ██████╗ ██╗   ██╗███╗   ██╗
# ╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║
#    ██║   ██║   ██║██████╔╝ ╚████╔╝ ██╔██╗ ██║
#    ██║   ██║   ██║██╔══██╗  ╚██╔╝  ██║╚██╗██║
#    ██║   ╚██████╔╝██████╔╝   ██║   ██║ ╚████║
#    ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═══╝
#         """
        self.printf(graph)
    def loadCasePrint(self,caseNameList):
        graph = "Load %s cases..."%len(caseNameList)
        self.printf(graph)
        graph = "Running..."
        self.printf(graph)