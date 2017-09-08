from troubleshooting.framework.remote.BashSSH import BaseSSH
class SSHLibrary(BaseSSH):
    def __init__(self):
        super(SSHLibrary,self).__init__()
    def read_file(self,file):
        stdout = self._execute_command("cat %s"%file)
        return stdout


if __name__ == "__main__":
    SSHLibrary()