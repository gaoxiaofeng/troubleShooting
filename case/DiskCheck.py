from _BaseCase import _BaseCase
class DiskCheck(_BaseCase):
    """
    To Check NBI3GC node disk usage.
    """
    def __init__(self):
        super(DiskCheck,self).__init__()
        self.passCondition = "{DiskSizeCheck} and {DiskInodesCheck}"
        self.tags = "n17.8 regression"



