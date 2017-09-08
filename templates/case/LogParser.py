from troubleshooting.framework.template._BaseCase import _BaseCase
class LogParser(_BaseCase):
    """
    To Check NBI3GC node disk usage.
    """
    def __init__(self):
        super(LogParser,self).__init__()
        self.passCondition = "{Nbi3gcERRORLogParse}"
        self.tags = "n17.8 regression"



