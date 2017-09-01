# -*- coding: utf-8 -*-
import  os
import re
import time,datetime


class  logParser(object):
    def __init__(self):
        super(logParser,self).__init__()
        self._log4j = None
        self._logPath = None
        self._errorLogs = []
        self._level = None
        self._logs = []
        self._classItem = []
        self._parsed_class_count = {}
        self._parsed_class_content = {}
    @property
    def log4j(self):
        return self._log4j
    @log4j.setter
    def log4j(self,file):
        if os.path.isfile(file):
            self._log4j = file
    @property
    def logPath(self):
        return  self._logPath
    @logPath.setter
    def logPath(self,path):
        if os.path.isdir(path):
            self._logPath = path
    def _listErrorLog(self):

        pattern = re.compile(r'oss_error.+\.log',re.M|re.S|re.I)
        for fileName in  os.listdir(self.logPath):
            absolute_path = os.path.join(self.logPath,fileName)
            if os.path.isfile(absolute_path) and pattern.match(fileName) :
                self._errorLogs.append(absolute_path)

    def _readLog(self,file):
        print file
        with open(file,"rb") as f:
            lines = f.readlines()
        data = "".join(lines)
        # pattern = re.compile(r"(\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2}\.\d{3}\+\d{4})",re.M|re.S)
        pattern = re.compile(r"(^\d{4}-\d{2}-\d{2}-T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{4})\s+\|\s+\S+\s+\|\s+\|\s+\S+\s+\|\s+(%s)\s+\|\s+(\S+)\s+\|\s+([\S \t]+)"%self._level, re.M | re.S)
        match = pattern.finditer(data)
        for m in match:
            _time = m.group(1)
            # _level = m.group(2)
            _class = m.group(3)
            _content = m.group(4)
            self._logs.append({"time":_time,"class":_class,"content":_content})


    def parseErrorLog(self):
        self._listErrorLog()
        self._level = "ERROR"
        for file in self._errorLogs:
            self._readLog(file)
        self._getClass()
        self.countClass()
        self.contentClass()

    def contentClass(self):

        for _log in self._logs:
            _class = _log["class"]
            _content = _log["content"]
            if self._parsed_class_content.has_key(_class):
                self._parsed_class_content[_class].update(set([_content]))
            else:
                self._parsed_class_content.update({_class:set([_content])})


    def _getClass(self):
        for _log in self._logs:
            self._classItem.append(_log["class"])

    def countClass(self):
        _class_set = set(self._classItem)
        for __class in _class_set:
            self._parsed_class_count.update({__class:self._classItem.count(__class)})


    def getResult(self):
        return self._parsed_class_content,self._parsed_class_count



if __name__ == "__main__":
    log = logParser()
    # log.logPath = "/var/opt/oss/log/nbi3gc"
    log.logPath = r"D:\userdata\jargao\Downloads"
    log.parseErrorLog()
    print log.getResult()[0]
    print log.getResult()[1]


