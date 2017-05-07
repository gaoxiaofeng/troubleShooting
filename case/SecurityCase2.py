from _BaseCase import _BaseCase
class SecurityCase2(_BaseCase):
    def __init__(self):
        super(SecurityCase2,self).__init__()
        self.passCondition = "{Security_001} is False"
        self.fixStep = ["stop nbi3gc","start nbi3gc"]
        self.describe = "To Check NBI3GC Function with IIOP Security "



