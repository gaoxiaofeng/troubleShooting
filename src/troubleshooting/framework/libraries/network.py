import urllib2
import urllib
class httpClient(object):
    def __init__(self):
        super(httpClient,self).__init__()
    def open(self,url):
       values = {"name":"test",
                "location":"",
                "language":"python"}
       data = urllib.urlencode(values)
       header = {"User-Agent":"TroubleShooting Framework"}
       req = urllib2.Request(url,data,header)
       response = urllib2.urlopen(req)
       the_page = response.read()
       return the_page
