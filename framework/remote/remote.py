import  paramiko
import os
from framework.library.library import getFileMd5
class Remote(object):
    def __init__(self):
        super(Remote,self).__init__()
        self._ssh = None
        self._sftp = None
        self._host = None
        self._port = None
        self._username = None
        self._password = None
        self._localFile = []
        self._localFolder = []
    def _connect(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(self._host,self._port,self._username,self._password)
    def _execute_command(self,command,returnCheck = False):
        stdin,stdout,stderr = self._ssh.exec_command(command)
        if not returnCheck:
            return stdout.read()
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
            localFileMd5 = getFileMd5(localFile)
            remoteFileMd5 = self._execute_command("md5sum %s"%remoteFile)
            if remoteFileMd5:
                remoteFileMd5 = remoteFileMd5.split(" ")[0]
            if remoteFileMd5 != localFileMd5:
                print "upload local file  %s" % localFile
                self._sftp_put(localFile,remoteFile)
        else:
            raise Exception("fail to sftp put file(%s) due to this file Not Found. "%localFile)
    def get(self,remoteFile,localFile):
        print "download remote file %s --> %s"%(remoteFile,localFile)
        self._sftp_get(remoteFile,localFile)
    def close_connection(self):
        self._close()
    def put_folder(self,folder):
        self._list_local_folder(folder)
        for _folder in self._localFolder:
            _folderConverted = self._pathConvert(_folder)
            self._mkdir(_folderConverted)
        for i,_file in enumerate(self._localFile):
            _fileConverted = self._pathConvert(_file)
            self.put(_file,_fileConverted)


    def _upload_tool(self):
        self._localHomeDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._remoteHomeDir = self._localHomeDir.split(os.path.sep)[-1]
        self.put_folder(self._localHomeDir)
    def _list_local_folder(self,folder):
        child_folders = os.listdir(folder)
        for child_folder in child_folders:
            if child_folder.startswith("."):
                continue
            if child_folder.endswith(".pyc"):
                continue
            if child_folder.endswith(".html"):
                continue
            if child_folder.endswith(".log"):
                continue
            child_folder_absolutely = os.path.join(folder,child_folder)
            if os.path.isfile(child_folder_absolutely):
                self._localFile.append(child_folder_absolutely)
            elif os.path.isdir(child_folder_absolutely):
                self._localFolder.append(child_folder_absolutely)
                self._list_local_folder(child_folder_absolutely)
            else:
                raise Exception("unkown path %s"%folder)

    def _pathConvert(self,path):
        _path = path.replace(os.path.dirname(self._localHomeDir),"").replace("\\","/")
        if not _path.startswith("."):
            _path = ".%s"%_path
        return  _path

    def _mkdir(self,path):
        command = "mkdir -p %s"%path
        self._execute_command(command)
    def _remote_running(self):
        print "running tool in remote machine"
        command = "cd %s;python runner.py  --print no"%self._remoteHomeDir
        self._execute_command(command)


    def _get_report(self):
        remote_report = "%s/report.html"%self._remoteHomeDir
        local_report = os.path.join(self._localHomeDir,"report_remote_%s.html"%self._host)
        self.get(remote_report,local_report)
    def remoteRunning(self):
        self._upload_tool()
        self._remote_running()
        self._get_report()


if __name__ == "__main__":
    r = Remote()
    r.open_connection("10.91.65.149",username=r"root",password=r"arthur")
    r.remoteRunning()
    r.close_connection()


