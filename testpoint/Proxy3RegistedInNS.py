from framework.libraries.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Proxy3RegistedInNS(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        # self.needRestartNbi3gcAfterFixed = True
        self._proxyId = PROXY.PROXY3
        self.level = LEVEL.CRITICAL

    def _checkpoint(self):
        proxyDeployedStatus = self.get_proxy_deploy_status(self._proxyId)
        if proxyDeployedStatus is False:
            print "%s was undeployed."%self._proxyId
            self.status = STATUS.PASS
            return
        irp_list = self.get_irp_from_ns(self._proxyId)
        print "%s IOR :%s"%(self._proxyId,irp_list)
        expert_irp_list = ["AlarmIRP","KernelCMIRP","BasicCMIRP","NotificationIRP",\
                               "EPIRP","CSIRP","FTIRP"]
        lost_irp_list = list(set(expert_irp_list) ^ set(irp_list) )
        if  "BulkCmIRP" in lost_irp_list :
            lost_irp_list.remove("BulkCmIRP")
        if lost_irp_list != []:
            print "%s missing %s IOR" % (self._proxyId, lost_irp_list)
            self.status = STATUS.FAIL
            self.IMPACT.append("Operator can not get IOR from namingService.")

            for lost_irp in lost_irp_list:
                self.RCA.append("%s IORs was lost in namingService"%lost_irp)
            self.FIXSTEP.append("#smanager.pl stop service nbi3gc")
            self.FIXSTEP.append("#smanager.pl start service nbi3gc")
        else:
            self.status = STATUS.PASS










