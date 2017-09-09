# -*- coding: utf-8 -*-
from troubleshooting.framework.output.output import OutPut
from troubleshooting.framework.libraries.library import  singleton
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance

@singleton
class welcome(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.printf = OutPut().echo
        self._totalWidth =  ConfigManagerInstance.config["report_total_width"]
        self._welcome()
    def _welcome(self):
        graph = r"""
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
        """
        graph = "*" * self._totalWidth
        self.printf(graph)
        graph = r"""
           ____
         / |   |\
  _____/ @ |   | \
 |> . .    |   |   \
  \  .     |||||     \________________________
   |||||||\                                    )
            \                                 |
             \                                |
               \                             /
                |   ____________------\     |
                |  | |                ||    /
                |  | |                ||  |
                |  | |                ||  |
                |  | |                ||  |     TroubleShooting Framework
               (__/_/                ((__/"""
        self.printf(graph)
    def loadCasePrint(self,caseNameList):
        graph = "Load %s cases..."%len(caseNameList)
        self.printf(graph)
        graph = "Running..."
        self.printf(graph)

