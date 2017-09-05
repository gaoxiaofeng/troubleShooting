from _BaseCase import _BaseCase
class LogParser(_BaseCase):
    """
    To Check NBI3GC node disk usage.
    """
    def __init__(self):
        super(LogParser,self).__init__()
        self.passCondition = "{nbi3gcLogParse}"
        self.tags = "n17.8 regression"



