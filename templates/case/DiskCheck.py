from troubleshooting.framework.template.Case import Case
class DiskCheck(Case):
    """
    To Check linux disk usage.
    """
    def __init__(self):
        super(DiskCheck,self).__init__()
        self.passCondition = "{DiskSizeCheck} and {DiskInodesCheck} and {ShouldBeExistTestFile}"
        self.tags = "template"



