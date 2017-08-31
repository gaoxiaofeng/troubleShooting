from _BaseCase import _BaseCase
class SecurityCheck(_BaseCase):
    """
    To Check NBI3GC Function with IIOP Security.
    """
    def __init__(self):
        super(SecurityCheck,self).__init__()
        condition = ["{SimulatorSecurityShouldBeMatched}","{nbiCodesetShouldBeMatch}","{Nbi3gcProxyKeyStoreConfigShouldBeSame}",\
                     "{Nbi3gcCipherShouldBeValid}","{SecurityShouldBeMatched}","{Nbi3gcCipherShouldBeMatched}",\
                     "{nbiKeyStoreShouldBeMatched}","{Nbi3gcomCipherShouldBeValid}"]
        self.passCondition = " and ".join(condition)
        self.tags = "n17.8 regression"




if __name__ == "__main__":
    SecurityCheck()