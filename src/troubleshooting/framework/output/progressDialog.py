# -*- coding: utf-8 -*-
import time
from troubleshooting.framework.output.output import OutPut
from threading import Thread
from troubleshooting.framework.variable.variable import *
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
            self.printf(content)
            if self._done == self._total:
                break
            time.sleep(0.01)
        if self._RUN:
            done = "#"*int(self._ratio*PROGREES_LENHTH)
            undone = " " *(PROGREES_LENHTH - int(self._ratio*PROGREES_LENHTH))
            content = "\rProgress:[%s%s]  %s/%s"%(done,undone,self._done,self._total)
            self.printf(content)
            self.printf("\tDone!\n")
    def stop(self):
        self._RUN = False