from output.output import OutPutQueue
from variable.variable import *
from library import Getch
import  time
import  re
class ControlView(object):
    def __init__(self):
        super(ControlView, self).__init__()
    def printf(self,message):
        OutPutQueue.put(message)
        while 1:
            if OutPutQueue.empty():
                break
    def __call__(self, *args):
        offset = 0
        maxOffset = len(args) -1
        shortKeyList = []
        selected = ""
        pattern = re.compile(r".*\[(.+)\].*")
        for option in args:
            match =  pattern.match(option)
            if match:
                shortKeyList.append(match.group(1).strip().lower())



        while 1:
            View = "\r\33[K"+ "".join(args).replace(args[offset],PRINT_REVERSE+args[offset]+PRINT_END)
            self.printf(View)
            inkey = Getch()
            key = inkey()
            if len(key) == 0:
                #windows CR
                continue

            if key in shortKeyList:
                selected = key
                break
            elif ord(key) == 10 or ord(key) == 13:
                selected = shortKeyList[offset]
                break
            elif ord(key) ==  65 or ord(key) == 68:
                #up/left
                if offset > 0:
                    offset -= 1
            elif ord(key) == 66 or ord(key) == 67:
                #down/right
                if offset < maxOffset:
                    offset += 1
            else:
                pass




        return  selected







