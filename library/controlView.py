from output.output import OutPutQueue
from variable.variable import *
from library import Getch
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
            View = r"\r"+ "".join(args).replace(args[offset],PRINT_HIGHLIGHT+args[offset]+PRINT_END)
            self.printf(View)
            inkey = Getch()
            key = inkey()

            if key in shortKeyList:
                selected = key
                break
            if key == "\n" or key == "\r\n":
                selected = shortKeyList[offset]
                break

        return  selected







