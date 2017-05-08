from _BaseCase import _BaseCase
class Security(_BaseCase):
    def __init__(self):
        super(Security,self).__init__()
        self.passCondition = "{Security_001} is True and {Security_002} is True"
        self.describe = "To Check NBI3GC Function with IIOP Security "



