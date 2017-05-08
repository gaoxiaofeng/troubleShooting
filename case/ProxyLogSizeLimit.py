from _BaseCase import _BaseCase
class ProxyLogSizeLimit(_BaseCase):
    def __init__(self):
        super(ProxyLogSizeLimit,self).__init__()
        self.passCondition = "{Proxy_log4j_check} is True"
        self.describe = "To Check Proxy(1,2,3) log size configration"



