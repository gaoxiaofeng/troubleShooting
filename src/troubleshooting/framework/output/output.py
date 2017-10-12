# -*- coding: utf-8 -*-
import threading
from Queue import Queue
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.variable.variable import *
OutPutQueue = Queue()
import re
from troubleshooting.framework.output.Print import CONSOLE

class Handler(object):
    def __init__(self):
        super(Handler,self).__init__()
        self._successor = None
        self.content = None

    @property
    def successor(self):
        return  self._successor
    @successor.setter
    def successor(self,successor):
        self._successor = successor
    def handle(self,content):
        self.content = content
        if self.successor is not None:
            self.successor.handle(content)


class ExceptionHandler(Handler):
    def __init__(self):
        super(ExceptionHandler,self).__init__()
    def handle(self,content):
        if "Exception" in content:
            content = COLOUR.Red.value + content + COLOUR.End.value
        super(ExceptionHandler,self).handle(content)



class ReservedWordHandler(Handler):
    def __init__(self):
        super(ReservedWordHandler,self).__init__()
        self.reservedWordList = ["Description:","TestPoints:","Result:","Fix Method:","Question:","Root Cause Analysis:",\
                                 "Impact Analysis:","[Critical]","[Minor]","Mandatory","Optional","|","*","Fix Method for Critical Problems:",\
                                 "Fix Method for Minor Problems:","Deailed Message:","ShortCut","CaseName:","Result",\
                                 "Case Deail List","Reference document:","index:"]
    def handle(self,content):
        for reservedWord in self.reservedWordList:
            if reservedWord in content:
                content = content.replace(reservedWord, COLOUR.Blue.value + reservedWord + COLOUR.End.value)
        super(ReservedWordHandler, self).handle(content)


class HighLightHandler(Handler):
    def __init__(self):
        super(HighLightHandler,self).__init__()
        #high light the contents in moddle of {}
    def handle(self,content):
        pattern_highLight = re.compile(r".*(\{.+\}).*", re.M | re.S)
        match_highLight = pattern_highLight.match(content)
        if match_highLight:
            highLight = match_highLight.group(1)
            highLight_strip = highLight.strip("{}")
            content = content.replace(highLight, COLOUR.HighLight.value + highLight_strip + COLOUR.End.value)
        super(HighLightHandler, self).handle(content)

class Client(object):
    def __init__(self):
        super(Client,self).__init__()

    def handle(self,content):
        h1 = ExceptionHandler()
        h2 = ReservedWordHandler()
        h3 = HighLightHandler()
        h1.successor = h2
        h2.successor = h3
        h1.handle(content)
        return h3.content

@singleton
class OutPut(threading.Thread):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.output = OutPutQueue
        self.running = True

    def printf(self,content):


        if content.strip():
            client = Client()
            content = client.handle(content)
            if  content[0] == "\r":
                # sys.stdout.write(content)
                # sys.stdout.flush()
                CONSOLE.write(content)
                CONSOLE.flush()
            else:
                self._print(content)
    def _print(self,content):
        CONSOLE.write(content + "\n")
        CONSOLE.flush()
    def echo(self,content):
        self._print(content)

    def stop(self):
        while 1:
            if self.output.empty():
                self.running = False
                break
    def run(self):
        while 1:
            if self.running:
                if not self.output.empty():
                    content = self.output.get(False)
                    self.printf(content)
            else:
                break



if __name__ == "__main__":
    pass
