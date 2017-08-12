import  paramiko
import os

class SFTP(object):
    def __init__(self):
        super(SFTP,self).__init__()
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
    def _execute_command(self,command):
        stdin,stdout,stderr = self._ssh.exec_command(command)
        if stderr:
            raise Exception("exec remote command error: %s"%stderr)
        else:
            return stdout
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

            self._sftp_put(localFile,remoteFile)
        elif os.path.isdir(localFile):
            self._execute_command("mkdir %s -p"%remoteFile)
        else:
            raise Exception("fail to sftp put file(%s) due to this file Not Found. "%localFile)
    def get(self,remoteFile,localFile):
        self._sftp_get(remoteFile,localFile)
    def close_connection(self):
        self._close()


if __name__ == "__main__":
    sftp = SFTP()
    sftp.open_connection("192.168.10.107",username="jarvan",password="newmedia")
    sftp.get("test","test")
    sftp.close_connection()

