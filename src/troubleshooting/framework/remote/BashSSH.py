# -*- coding: utf-8 -*-
import  paramiko
import os
from troubleshooting.framework.libraries.library import getFileMd5
class BaseSSH(object):
    def __init__(self):
        super(BaseSSH,self).__init__()
        self._ssh = None
        self._sftp = None
        self._host = None
        self._port = None
        self._username = None
        self._password = None
    def _connect(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(self._host,self._port,self._username,self._password)
    def _execute_command(self,command,checkerr = False):
        stdin,stdout,stderr = self._ssh.exec_command(command)
        if not checkerr:
            return stdout.read()
        if stderr.read():
            raise Exception("exec remote command error: %s"%stderr.read())
        else:
            return stdout.read()
    def _openSftp(self):
        t = paramiko.Transport(sock=(self._host,self._port))
        t.connect(username=self._username,password=self._password)
        self._sftp = paramiko.SFTPClient.from_transport(t)
    def _sftp_get(self,remoteFile,localFile):
        if self._sftp:
            self._sftp.get(remoteFile,localFile)
        else:
            raise Exception("please open connection before sftp get.")
    def _sftp_put(self,localFile,remoteFile):
        if self._sftp:
            self._sftp.put(localFile,remoteFile)
        else:
            raise Exception("please open connection before sftp put")
    def _close(self):
        if self._ssh:
            self._ssh.close()
            self._ssh = None

    def open_connection(self,host,port=22,username="root",password="arthur"):
        if not isinstance(host,str) or not host:
            raise Exception("fail to open connection, host is %s"%host)
        if not isinstance(port,int) or not port:
            raise Exception("fail to open connection, port is %s"%host)
        if not isinstance(username,str) or not port:
            raise Exception("fail to open connection, port is %s"%host)
        if not isinstance(password,str) or not port:
            raise Exception("fail to open connection, port is %s"%host)
        self._host,self._port,self._username,self._password = host,port,username,password
        self._connect()
        self._openSftp()
    def put(self,localFile,remoteFile):
        if os.path.isfile(localFile):
            localFileMd5 = getFileMd5(localFile)
            remoteFileMd5 = self._execute_command("md5sum %s"%remoteFile)
            if remoteFileMd5:
                remoteFileMd5 = remoteFileMd5.split(" ")[0]
            if remoteFileMd5 != localFileMd5:
                # print "upload local file  %s" % localFile
                self._sftp_put(localFile,remoteFile)
        else:
            raise Exception("fail to sftp put file(%s) due to this file Not Found. "%localFile)
    def get(self,remoteFile,localFile):
        # print "download remote file %s --> %s"%(remoteFile,localFile)
        self._sftp_get(remoteFile,localFile)
    def close_connection(self):
        self._close()