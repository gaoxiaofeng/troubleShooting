# -*- coding: utf-8 -*-
from framework.output.output import OutPut
from framework.library.library import  singleton
from framework.configuration import  ConfigManagerInstance
from threading import  Thread
from framework.variable.variable import *
import time
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
#         graph = r"""
# ████████╗ ██████╗ ██████╗ ██╗   ██╗███╗   ██╗
# ╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║
#    ██║   ██║   ██║██████╔╝ ╚████╔╝ ██╔██╗ ██║
#    ██║   ██║   ██║██╔══██╗  ╚██╔╝  ██║╚██╗██║
#    ██║   ╚██████╔╝██████╔╝   ██║   ██║ ╚████║
#    ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═══╝
#         """
#         graph = """
#      _  _  ____  __     ___  __   _  _  ____
#     / )( \(  __)(  )   / __)/  \ ( \/ )(  __)
#     \ /\ / ) _) / (_/\( (__(  O )/ \/ \ ) _)
#     (_/\_)(____)\____/ \___)\__/ \_)(_/(____)
# """
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
        graph = "Load %s cases..."%len(caseNameList)
        self.printf(graph)
        graph = "Running..."
        self.printf(graph)

class ProgressDialog(Thread):
    def __init__(self,total):
        super(ProgressDialog,self).__init__()
        self._total = total
        self._done = 0
        self._ratio = 0
        self._RUN = True
        self.printf = OutPut().printf
    def set(self):
        return self._done
    def set(self,num):
        if isinstance(num,int):
            self._done = num
            self._ratio = float(self._done)/float(self._total)
        else:
            print "Progress is not int",num
    def run(self):
        while self._RUN:
            done = "#"*int(self._ratio*PROGREES_LENHTH)
            undone = " " *(PROGREES_LENHTH - int(self._ratio*PROGREES_LENHTH))
            content = "\rProgress:[%s%s]  %s/%s"%(done,undone,self._done,self._total)
            # sys.stdout.write("\rProgress:[%s%s]  %s/%s"%(done,undone,self._done,self._total))
            # sys.stdout.flush()
            self.printf(content)
            if self._done == self._total:
                break
            time.sleep(0.01)
        if self._RUN:
            # sys.stdout.write( "\tSuccess.\n")
            self.printf("\tDone.\n")
    def stop(self):
        self._RUN = False