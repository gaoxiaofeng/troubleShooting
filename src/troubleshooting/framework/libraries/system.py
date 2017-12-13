# -*- coding: utf-8 -*-
import os
import shutil
import traceback
import hashlib
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.libraries.baseList import anyElement2StringForList
import time
from  os.path import join,dirname,abspath
def createDir(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except Exception,e:
            raise IOError(e)
def removeDir(path):
    try:
        shutil.rmtree(path)
    except Exception, e:
        logger().error(traceback.format_exc())
def removeFile(path):
    try:
        os.remove(path)
    except Exception,e:
        logger().error(traceback.format_exc())
def clean(path=os.getcwd()):
    for file in os.listdir(path):
        absolute_path = os.path.join(path, file)
        if os.path.isdir(absolute_path):
            # if len(file) == 7 and file.endswith(".d"):
            #     #clean for report directory
            #     removeDir(absolute_path)
            if file == ".temp":
                #clean for .temp directory
                removeDir(absolute_path)
            if file == "www":
                #clean for cig-bin directory
                removeDir(absolute_path)
def auto_clean(path=join(os.getcwd(),"www")):
    reportindexList = []
    reportDict = {}
    if not os.path.exists(path):
        return
    for file in os.listdir(path):
        absolute_path = os.path.join(path, file)
        if os.path.isdir(absolute_path):
            if len(file) == 7 and file.endswith(".d"):
                fileCreateTimeStamp = get_FileCreateTimeStamp(absolute_path)
                reportindexList.append(fileCreateTimeStamp)
                reportDict[str(fileCreateTimeStamp)] = absolute_path
    if len(reportindexList) > 10:
        reportindexList.sort()
        reportindexList = anyElement2StringForList(reportindexList)
        need_delete_number = len(reportindexList) - 10
        for index in range(need_delete_number):
            need_delete_file_path = reportDict[reportindexList[index]]
            removeDir(need_delete_file_path)








def copyFile(old,new):
    with open(old, "rb") as f:
        content = f.read()
    with open(new, "wb") as f:
        f.write(content)
def copyDir(left,right):
    if not  os.path.isdir(left):
        print "Directory %s is not exist."%left
        return
    if not os.path.isdir(right):
        createDir(right)

    for file in os.listdir(left):
        left_absolute_path = os.path.join(left, file)
        right_absolute_path = os.path.join(right,file)
        if os.path.isfile(left_absolute_path):
            copyFile(left_absolute_path,right_absolute_path)
        if os.path.isdir(left_absolute_path):
            copyDir(left_absolute_path,right_absolute_path)
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return  time.strftime("%Y-%m-%d %H:%M:%S",timeStruct)
def get_FileCreateTime(path):
    filepath = unicode(path,"utf8")
    t = os.path.getctime(filepath)
    return  TimeStampToTime(t)
def get_FileModifyTime(path):
    filepath = unicode(path,"utf8")
    t = os.path.getmtime(filepath)
    return TimeStampToTime(t)
def get_FileCreateTimeStamp(path):
    filepath = unicode(path,"utf8")
    t = os.path.getctime(filepath)
    return t
def  getFileMd5(filename):
    if not os.path.isfile(filename):
        raise Exception("failed to get file md5, reason :%s is not a file"%filename)
    myhash = hashlib.md5()
    with open(filename,"rb") as f:
        content = f.read()
        myhash.update(content)
    return  myhash.hexdigest()