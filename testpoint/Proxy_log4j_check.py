from library.library import singleton,conversion
from manager import EngineManagerInstance
from variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class Proxy_log4j_check(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.describe = "proxy(1,2,3) logs size limit: info log 10M *5, trace log 10M *10, error log 10M *5. "
        self.level = NOCRITICAL

    def _checkpoint(self):
        get_dict_from_xml = EngineManagerInstance.get_keyword("get_dict_from_xml")
        proxy1_log4j = "/opt/oss/NSN-nbi3gc/proxy-1/etc/log4j.xml"
        value = get_dict_from_xml(proxy1_log4j)
        proxy1_info_log = value["mf-info"]
        proxy1_trace_log = value["mf-trace"]
        proxy1_error_log = value["mf-error"]
        proxy1_info_log_size = proxy1_info_log["maxFileSize"]
        proxy1_trace_log_size = proxy1_trace_log["maxFileSize"]
        proxy1_error_log_size = proxy1_error_log["maxFileSize"]
        proxy1_info_log_index = proxy1_info_log["maxBackupIndex"]
        proxy1_trace_log_index = proxy1_trace_log["maxBackupIndex"]
        proxy1_error_log_index = proxy1_error_log["maxBackupIndex"]
        proxy1_info_log_maxSize = conversion(proxy1_info_log_size) * int(proxy1_info_log_index)
        proxy1_trace_log_maxSize = conversion(proxy1_trace_log_size) * int(proxy1_trace_log_index)
        proxy1_error_log_maxSize = conversion(proxy1_error_log_size) * int(proxy1_error_log_index)
        if proxy1_info_log_maxSize > conversion("50MB"):
            self.status = FAIL
            self.IMPACT.append("disk /var usage too much.")
            self.RCA.append("proxy-1 log size configuration over limit. > 50MB")
            self.FIXSTEP.append("reset %s info level log to under 50MB"%proxy1_log4j)
        else:
            self.status = PASS

