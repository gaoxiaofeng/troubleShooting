from _BaseCase import _BaseCase
class ProxyLogSizeLimit(_BaseCase):
    """
    To Check configuration maxFileSize for Proxy-1,Proxy-2 and Proxy-3.
    """
    def __init__(self):
        super(ProxyLogSizeLimit,self).__init__()
        self.passCondition = "{Proxy1Log4jCheck} is True and {Proxy2Log4jCheck} is True and {Proxy3Log4jCheck} is True"
        self.referenceDocument = "https://pronto.int.net.nokia.com/pronto/problemReportSearch.html?freeTextdropDownID=prId&searchTopText=PR222307&HomeFlag=true"


