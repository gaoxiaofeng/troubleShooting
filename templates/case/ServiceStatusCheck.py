from troubleshooting.framework.template._BaseCase import _BaseCase
class ServiceStatusCheck(_BaseCase):
    """
    To Check NBI3GC and NBI3GCOM Process Status
    """
    def __init__(self):
        super(ServiceStatusCheck,self).__init__()
        self.passCondition = "{Nbi3gcServiceCheck} and {Nbi3gcomServiceCheck}"
        self.tags = "n17.8 regression basic"



