from _BaseCase import _BaseCase
class SecurityCase(_BaseCase):
    def __init__(self):
        super(SecurityCase,self).__init__()
        self.passCondition = "{Security_001} is True and {Security_002} is True"
        self.fixStep = ["stop nbi3gc","start nbi3gc"]
        self.describe = "To Check NBI3GC Function with IIOP Security "



