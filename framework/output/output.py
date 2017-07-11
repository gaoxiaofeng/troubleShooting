import sys,os
##from manager import TestPointManager,EngineManager,CaseManager
import threading
from Queue import Queue
from framework.library.library import singleton
from framework.variable.variable import *
OutPutQueue = Queue()
import re



class Handler(object):
    def __init__(self):
        super(Handler,self).__init__()
        self._successor = None
    @property
    def successor(self):
        return  self._successor
    @successor.setter
    def successor(self,successor):
        self._successor = successor
    def handle(self):
        pass

class ExceptionHandler(Handler):
    def __init__(self):
        super(ExceptionHandler,self).__init__()
    def handle(self,content):
        if "Exception" in content:
            content = COLOUR.Red + content + COLOUR.End
        self.successor.handle(content)



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
                content = content.replace(reservedWord, COLOUR.Blue + reservedWord + COLOUR.End)
        self.successor.handle(content)


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
            content = content.replace(highLight, COLOUR.HighLight + highLight_strip + COLOUR.End)
        self.successor.handle(content)
class FinalHandler(Handler):
    def __init__(self):
        super(FinalHandler,self).__init__()
        self._content = None
    def handle(self,content):
        self._content = content
    @property
    def content(self):
        return self._content
    @content.setter
    def content(self,content):
        pass
class Client(object):
    def __init__(self):
        super(Client,self).__init__()

    def handle(self,content):
        h1 = ExceptionHandler()
        h2 = ReservedWordHandler()
        h3 = HighLightHandler()
        final = FinalHandler()
        h1.successor = h2
        h2.successor = h3
        h3.successor = final
        h1.handle(content)
        return final.content

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
                sys.stdout.write(content)
                sys.stdout.flush()
            else:
                print content
    def echo(self,content):
        print content

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
