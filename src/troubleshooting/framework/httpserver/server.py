import BaseHTTPServer,CGIHTTPServer
from threading import  Thread
import os
import urllib
from os.path import abspath,dirname,join
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
from troubleshooting.framework.libraries.system import createDir,copyFile
from troubleshooting.framework.log.logger import logger
class CGIHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ['/cgi-bin', '/htbin','/www']
    def log_message(self, format, *args):
        logger().info(format%args)
    def is_cgi(self):
        """Test whether self.path corresponds to a CGI script.

        Returns True and updates the cgi_info attribute to the tuple
        (dir, rest) if self.path requires running a CGI script.
        Returns False otherwise.

        If any exception is raised, the caller should assume that
        self.path was rejected as invalid and act accordingly.

        The default implementation tests whether the normalized url
        path begins with one of the strings in self.cgi_directories
        (and the next character is a '/' or the end of the string).
        """
        if "?" in  self.path:
            #included args
            file = self.path.split("?")[0]
        else:
            file = self.path
        if file.endswith("py"):
            collapsed_path = _url_collapse_path(self.path)
            dir_sep = collapsed_path.find('/', 1)
            head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep + 1:]
            self.cgi_info = head, tail
            return True
        else:
            return False
def _url_collapse_path(path):
    """
    Given a URL path, remove extra '/'s and '.' path elements and collapse
    any '..' references and returns a colllapsed path.

    Implements something akin to RFC-2396 5.2 step 6 to parse relative paths.
    The utility of this function is limited to is_cgi method and helps
    preventing some security attacks.

    Returns: The reconstituted URL, which will always start with a '/'.

    Raises: IndexError if too many '..' occur within the path.

    """
    # Query component should not be involved.
    path, _, query = path.partition('?')
    path = urllib.unquote(path)

    # Similar to os.path.split(os.path.normpath(path)) but specific to URL
    # path semantics rather than local operating system semantics.
    path_parts = path.split('/')
    head_parts = []
    for part in path_parts[:-1]:
        if part == '..':
            head_parts.pop() # IndexError if more '..' than prior parts
        elif part and part != '.':
            head_parts.append( part )
    if path_parts:
        tail_part = path_parts.pop()
        if tail_part:
            if tail_part == '..':
                head_parts.pop()
                tail_part = ''
            elif tail_part == '.':
                tail_part = ''
    else:
        tail_part = ''

    if query:
        tail_part = '?'.join((tail_part, query))

    splitpath = ('/' + '/'.join(head_parts), tail_part)
    collapsed_path = "/".join(splitpath)

    return collapsed_path
class server(Thread):
    def __init__(self):
        super(server,self).__init__()
        self.server = None
        self.home = dirname(abspath(__file__))
    def run(self,port=8888):
        # self.copy_report_to_home()
        self.deploy_cgi()
        # os.chdir(self.home)
        self.server = BaseHTTPServer.HTTPServer(("",port),CGIHandler )
        self.server.serve_forever()
    def terminate(self):
        raise RuntimeError("raise SystemExit from terminate commands")
    def stop(self):
        # self.terminate()
        self.server.shutdown()
        self.terminate()
    def copy_report_to_home(self):
        report = ConfigManagerInstance.config["Report"]
        with open(report,"rb") as f:
            content = f.read()
        finally_report = join(self.home,"index.html")
        with open(finally_report,"wb") as f:
            f.write(content)
    def deploy_cgi(self):
        # report = ConfigManagerInstance.config["Report"]
        # reportDir = dirname(report)
        cgi_bin_path = join(os.getcwd(),"www","cgi-bin")
        js_path = join(os.getcwd(),"www","js")
        createDir(cgi_bin_path)
        createDir(js_path)
        cgiOldFile = join(self.home,"www","cgi-bin","post.py")
        cgiNewFile = join(cgi_bin_path,"post.py")
        jsOldFile = join(self.home,"www","js","spin.min.js")
        jsNewFile = join(js_path,"spin.min.js")
        copyFile(cgiOldFile,cgiNewFile)
        copyFile(jsOldFile, jsNewFile)



if __name__ == "__main__":
    S = server()
    S.start()