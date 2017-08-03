from _BaseCase import _BaseCase
class SecurityCheck(_BaseCase):
    """
    To Check NBI3GC Function with IIOP Security.
    """
    def __init__(self):
        super(SecurityCheck,self).__init__()
        self.passCondition = "{SecurityShouldBeMatched} and {SimulatorSecurityShouldBeMatched} and {Nbi3gcProxyKeyStoreConfigShouldBeSame} and {nbiKeyStoreShouldBeMatched} and {nbiCodesetShouldBeMatch}"



