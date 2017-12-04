# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.log.logger import logger
import traceback
import time
@singleton
class ThreadManager(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.__thread_list = []
    def start(self,thread):
        thread.start()
        id = len(self.__thread_list)
        self.__thread_list.append(thread)
        return id
    def get_threads(self):
        return self.__thread_list
    def stop_all(self):
        for _thread in self.__thread_list:
            try:
                if _thread.isAlive():
                    _thread.stop()
            except Exception,e:
                logger().error(traceback.format_exc())
                status = False
            else:
                while 1:
                    time.sleep(0.1)
                    if not _thread.isAlive():
                        break
                status = True
        return status


    def stop(self,no):
        _thread = self.__thread_list[no]
        try:
            if _thread.isAlive():
                _thread.stop()
        except Exception, e:
            logger().error(traceback.format_exc())
            status = False
        else:
            while 1:
                time.sleep(0.1)
                if not _thread.isAlive():
                    break
            status = True
        return status
    def join(self,no):
        _thread = self.__thread_list[no]
        while 1:
            # wait for thread exit
            if _thread.is_alive():
                time.sleep(0.01)
            else:
                break

    def join_all(self):
        for _thread in self.__thread_list:
            if not _thread.isAlive():
                continue
            else:
                time.sleep(0.1)
