# -*- coding: utf-8 -*-
import logging,os
def singleton(cls,*args,**kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args,**kw)
        return instances[cls]
    return _singleton
@singleton
class logger(object):
    def __init__(self):
        fileName = "troubleshooting.log"
        if os.path.isfile(fileName):
            os.remove(fileName)
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(fileName)
        fh.setLevel(logging.DEBUG)
        formatter_fh = logging.Formatter(fmt="|%(asctime)-20s|%(name)-20s|%(levelname)-10s| %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter_fh)
        self._log.addHandler(fh)
        self.info("^"*100)

    def info(self,mesg):
        self._log.info(mesg)
    def warn(self,mesg):
        self._log.warn(mesg)
    def error(self,mesg):
        self._log.error(mesg)
    def debug(self,mesg):
        self._log.debug(mesg)
    def write(self,mesg):
        if mesg.strip():
            self._log.info(mesg)
    def flush(self):
        pass


if __name__ == "__main__":
    log = logger()
    log.info("init log...")
    log.warn("init log...")
    log.error("init log...")