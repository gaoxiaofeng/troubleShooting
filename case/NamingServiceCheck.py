from _BaseCase import _BaseCase
class NamingServiceCheck(_BaseCase):
    """
    To Check NBI3GC Function with IIOP Security.
    """
    def __init__(self):
        super(NamingServiceCheck,self).__init__()
        self.passCondition = "{Proxy1RegistedInNS} and {Proxy2RegistedInNS} and {Proxy3RegistedInNS}"



