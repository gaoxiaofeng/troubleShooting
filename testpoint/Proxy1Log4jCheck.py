from library.library import singleton,conversion
from manager import EngineManagerInstance
from variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Proxy1Log4jCheck(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.describe = "proxy-1 logs size limit: info log 10M *5, trace log 10M *10, error log 10M *5. "
        self.level = NOCRITICAL

    def _checkpoint(self):
        get_dict_from_xml = EngineManagerInstance.get_keyword("get_dict_from_xml")
        proxy_log4j = "/opt/oss/NSN-nbi3gc/proxy-1/etc/log4j.xml"
        value = get_dict_from_xml(proxy_log4j)
        proxy_info_log = value["mf-info"]
        proxy_trace_log = value["mf-trace"]
        proxy_error_log = value["mf-error"]
        proxy_info_log_size = proxy_info_log["maxFileSize"]
        proxy_trace_log_size = proxy_trace_log["maxFileSize"]
        proxy_error_log_size = proxy_error_log["maxFileSize"]
        proxy_info_log_index = proxy_info_log["maxBackupIndex"]
        proxy_trace_log_index = proxy_trace_log["maxBackupIndex"]
        proxy_error_log_index = proxy_error_log["maxBackupIndex"]
        proxy_info_log_maxSize = conversion(proxy_info_log_size) * int(proxy_info_log_index)
        proxy_trace_log_maxSize = conversion(proxy_trace_log_size) * int(proxy_trace_log_index)
        proxy_error_log_maxSize = conversion(proxy_error_log_size) * int(proxy_error_log_index)

        if proxy_info_log_maxSize > conversion("50MB"):
            self.status = FAIL
            self.IMPACT.append("disk /var usage over limit for 3GPP Corba FM.")
            self.RCA.append("The maxFileSize of proxy-1 Info logs over limit. (> 50MB)")
            self.FIXSTEP.append("reset configuration %s Info logs maxFileSize to under 50MB."%proxy_log4j)


        if proxy_trace_log_maxSize > conversion("100MB"):
            self.status = FAIL
            self.IMPACT.append("disk /var usage over limit for 3GPP Corba FM.")
            self.RCA.append("The maxFileSize of proxy-1 Trace logs over limit. (> 100MB)")
            self.FIXSTEP.append("reset configuration %s Trace logs maxFileSize to under 100MB." % proxy_log4j)

        if proxy_error_log_maxSize > conversion("50MB"):
            self.status = FAIL
            self.IMPACT.append("disk /var usage over limit for 3GPP Corba FM.")
            self.RCA.append("The maxFileSize of proxy-1 Error logs over limit. (> 50MB)")
            self.FIXSTEP.append("reset configuration %s Error logs maxFileSize to under 50MB." % proxy_log4j)
        if self.status is not FAIL:
            self.status = PASS