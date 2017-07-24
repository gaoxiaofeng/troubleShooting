from _BaseCase import _BaseCase
class SecurityCheck(_BaseCase):
    """
    To Check NBI3GC Function with IIOP Security.
    """
    def __init__(self):
        super(SecurityCheck,self).__init__()
        self.passCondition = "{SecurityShouldBeMatched} is True and {SimulatorSecurityShouldBeMatched} is True and {Nbi3gcProxyKeyStoreConfigShouldBeSame} is True and {nbiKeyStoreShouldBeMatched} is True"



