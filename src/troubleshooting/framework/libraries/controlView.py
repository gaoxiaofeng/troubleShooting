# -*- coding: utf-8 -*-
from troubleshooting.framework.output.output import OutPutQueue
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.libraries.library import Getch
import  re
class ControlView(object):
    def __init__(self,mode = LISTMODE,width = 20):
        super(ControlView, self).__init__()
        self.mode = mode #LINEMODE,LISTMODE
        self.width = width
    def printf(self,message):
        OutPutQueue.put(message)
        while 1:
            if OutPutQueue.empty():
                break
    def __LineMode__(self,*args):
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
            View = "\r\33[K"+ "".join(args).replace(args[offset],COLOUR.Reverse.value+args[offset]+COLOUR.End.value)
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


    def __ListMode__(self,*args):
        _args = []
        for option in args:
            if len(option)  < self.width:
                option = option + " "*(self.width - len(option))
                _args.append(option)
            else:
                _args.append(option)
        args = _args
        KeyMap = {}
        offset = 0
        maxOffset = len(args) -1
        shortKeyList = []
        selected = ""
        pattern = re.compile(r".*\[(.+)\].*")
        for option in args:
            match =  pattern.match(option)
            if match:
                shortKey = match.group(1).strip().lower()
                shortKeyList.append(shortKey)
                KeyMap[shortKey] = option
        i = 0
        while 1:
            View = "\n".join(args).replace(args[offset],COLOUR.Reverse.value + args[offset] + COLOUR.End.value) + "\33[K\33[?25l" + COLOUR.End.value
            if i == 0:
                # View = "\r|" + View
                View = "\r" + View
            else:
                # View = "\r|\33[%sA"%maxOffset + View
                View = "\r\33[%sA" % maxOffset + View
            i += 1
            self.printf(View)
            inkey = Getch()
            key = inkey()
            if len(key) == 0:
                #windows CR
                continue

            if key in shortKeyList:
                if "+" in KeyMap[key] or "Exit" in KeyMap[key]:
                    selected = key
                    break
            elif ord(key) == 10 or ord(key) == 13:
                if "+" in KeyMap[shortKeyList[offset]] or "Exit" in KeyMap[shortKeyList[offset]]:
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
        self.printf(chr(28))
        return  selected
    def __call__(self, *args):
        if self.mode == LINEMODE:
            selected = self.__LineMode__(*args)

        if self.mode == LISTMODE:
            selected = self.__ListMode__(*args)
        return  selected









