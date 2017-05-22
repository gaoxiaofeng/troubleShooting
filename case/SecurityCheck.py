from _BaseCase import _BaseCase
class SecurityCheck(_BaseCase):
    def __init__(self):
        super(SecurityCheck,self).__init__()
        self.passCondition = "{SecurityShouldBeMatched} is True and {SimulatorSecurityShouldBeMatched} is True"
        self.describe = "To Check NBI3GC Function with IIOP Security "
        self._internalCase = True



