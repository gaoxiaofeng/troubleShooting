# -*- coding: utf-8 -*-
import  os
import re
import time,datetime
from keywords._BaseKeyword import _BaseKeyword


class  logParser(_BaseKeyword):
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
        self.temp =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"framework","temp")



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
        if not path.endswith("/"):
            path = path + "/"
        self._logPath = path
    def _listErrorLog(self,logPath):

        pattern = re.compile(r'oss_error.+\.log',re.M|re.S|re.I)
        for fileName in  os.listdir(logPath):
            absolute_path = os.path.join(logPath,fileName)
            if os.path.isfile(absolute_path) and pattern.match(fileName) :
                self._errorLogs.append(absolute_path)
    def _readLog(self,file):
        # print file
        with open(file,"rb") as f:
            lines = f.readlines()
        data = "".join(lines)
        # pattern = re.compile(r"(\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2}\.\d{3}\+\d{4})",re.M|re.S)
        # P = r"(^\d{4}-\d{2}-\d{2}-T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{4})\s+\|\s+\S+\s+\|\s+\|\s+\S+\s+\|\s+(%s)\s+\|\s+(\S+)\s+\|\s+([\S \t]+)"%self._level
        P = r"(^\d{4}-\d{2}-\d{2}-T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{4})\s+\|[^\|]+\|[^\|]+\|[^\|]+\|\s+(%s)\s+\|\s+(\S+)\s+\|\s+([\S \t]+)" % self._level
        pattern = re.compile(P, re.M | re.S)
        match = pattern.finditer(data)
        for m in match:
            _time = m.group(1)
            # _level = m.group(2)
            _class = m.group(3)
            _content = m.group(4)
            self._logs.append({"time":_time,"class":_class,"content":_content})

    def _downloadLog(self):
        zipName = "log_%s.zip"%int(time.time())
        command = "zip -r %s %s/oss_error*.log;"%(zipName,self.logPath)
        stdout = self.execute_command(command)
        localPath = os.path.join(self.temp,zipName)
        self.download(zipName,localPath)
        self._zipFile(localPath)
    def _zipFile(self,fileName):
        import zipfile
        path = os.path.dirname(fileName)
        zfile = zipfile.ZipFile(fileName,"r")
        for _file in zfile.namelist():
            if _file.endswith("/"):
                continue
            if "/" in _file:
                __fileName = _file.split("/")[-1]
            else:
                __fileName = _file
            _filePath = os.path.join(path,__fileName)
            with open(_filePath,"w") as f:
                f.write(zfile.read(_file))

    def _cleanTemp(self):
        for _file in os.listdir(self.temp):
            _path = os.path.join(self.temp, _file)
            if os.path.isfile(_path):
                os.remove(_path)
            if os.path.isdir(_path):
                os.rmdir(_path)

    def _initTempfolder(self):
        if not os.path.isdir(self.temp):
            os.mkdir(self.temp)

    def parseErrorLog(self):
        if self.remote:
            self._initTempfolder()
            self._cleanTemp()
            self._downloadLog()
        self._listErrorLog(self.temp if self.remote else self.logPath)
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


    def getLogParsedResult(self,logPath,level="ERROR"):
        self._level = level
        self.logPath = logPath
        self.parseErrorLog()
        return self._parsed_class_content,self._parsed_class_count



if __name__ == "__main__":
    log = logParser()
    # log.logPath = "/var/opt/oss/log/nbi3gc"
    log.logPath = r"D:\userdata\jargao\Downloads"
    log.parseErrorLog()
    print log.getResult()[0]
    print log.getResult()[1]


