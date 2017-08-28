# -*- coding: utf-8 -*-
from framework.output.output import OutPut
from framework.libraries.library import  singleton
from framework.modules.configuration import  ConfigManagerInstance

@singleton
class welcome(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.printf = OutPut().echo
        self._totalWidth =  ConfigManagerInstance.config["report_total_width"]
        self._welcome()
    def _welcome(self):
        if not ConfigManagerInstance.config["Console"]:
            return
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
                |  | |                ||  |     3GPP Corba FM Sniffer
               (__/_/                ((__/"""
        self.printf(graph)
    def loadCasePrint(self,caseNameList):
        if not ConfigManagerInstance.config["Console"]:
            return
        graph = "Load %s cases..."%len(caseNameList)
        self.printf(graph)
        graph = "Running..."
        self.printf(graph)

