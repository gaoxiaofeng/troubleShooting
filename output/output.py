import sys,os
##from manager import TestPointManager,EngineManager,CaseManager
import threading
from Queue import Queue
from library.library import singleton
from variable.variable import *
OutPutQueue = Queue()
import re
@singleton
class OutPut(threading.Thread):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.output = OutPutQueue
        self.running = True
        self.reservedWordList = ["Description:","TestPoints:","Result:","Fix Method:","Question:","Root Cause Analysis:",\
                                 "Impact Analysis:","[Critical]","[Minor]","Mandatory","Optional","|","*","Fix Method for Critical Problems:",\
                                 "Fix Method for Minor Problems:","Deailed Message:","ShortCut","CaseName:","Result",\
                                 "Case Deail List","Reference document:","index:"]

    def printf(self,content):

        if content.strip():
            # if "\n" in content:
            #     content = content.replace("\n","\n|")
            if "Exception" in content:
                content = PRINT_RED  +  content + PRINT_END
            if  PASS in content:
                if "--*" in content:
                    content = content.replace(PASS,PRINT_GREEN + OK + PRINT_END)
                else:
                    content = content.replace(PASS,PRINT_GREEN_BLOD + PASS + PRINT_END)


            elif  FAIL in content:
                if "--*" in content:
                    content = content.replace(FAIL,PRINT_RED + ERROR + PRINT_END)
                else:
                    content = content.replace(FAIL,PRINT_RED_FLASH +  FAIL + PRINT_END)
            else:
                pass

            for reservedWord in self.reservedWordList:
                if reservedWord in content:
                    content = content.replace(reservedWord,PRINT_BLUE+reservedWord+PRINT_END)
            pattern_highLight = re.compile(r".*(\{.+\}).*",re.M|re.S)
            match_highLight = pattern_highLight.match(content)
            if match_highLight:
                highLight = match_highLight.group(1)
                highLight_strip = highLight.strip("{}")
                content = content.replace(highLight,PRINT_HIGHLIGHT+highLight_strip+PRINT_END)
            #if "[Input Selected]:" in content:
            #    content =  content.replace("[Input Selected]:",PRINT_YELLOW+"[Input Selected]:"+PRINT_END)
            #    sys.stdout.write(content)
            #    sys.stdout.flush()
            #    return

            if  content[0] == "\r":
                sys.stdout.write(content)
                sys.stdout.flush()
                return

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
    a = """

    |
    \--* Step 12. ![PASS]"""

    o = OutPut()
    o.printf(a)
