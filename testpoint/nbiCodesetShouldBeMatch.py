from framework.library.library import singleton
from framework.variable.variable import *
from _BaseTestPoint import _BaseTestPoint
@singleton
class nbiCodesetShouldBeMatch(_BaseTestPoint):
    """
    check nbi3gc and nbi3gcom codeset
    """
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.NOCRITICAL
        # self.needRestartNbi3gcAfterFixed = True
        # self.needRestartNbi3gcomAfterFixed = True

    def _checkpoint(self):
        codeSetenableItem = "jacorb.codeset"
        codeSetItem = "jacorb.native_char_codeset"

        self._nbi3gc_codeSet_enable = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,codeSetenableItem)
        self._nbi3gcom_codeSet_enable = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,codeSetenableItem)
        self._nbi3gc_codeSet = self.get_value_from_configuration(NBI3GC_MF_JACORB_PROPERTIES,codeSetItem)
        self._nbi3gcom_codeSet = self.get_value_from_configuration(NBI3GCOM_PROPERTIES,codeSetItem)
        print "nbi3gc codeset enable is %s"%self._nbi3gc_codeSet_enable
        print  "nbi3gcom codeset enable is %s"%self._nbi3gcom_codeSet_enable
        if self._nbi3gc_codeSet_enable == "on" and self._nbi3gcom_codeSet_enable == "on":
            print "nbi3gc codeset is %s"%self._nbi3gc_codeSet
            print "nbi3gcom codeset is %s"%self._nbi3gcom_codeSet
            if self._nbi3gc_codeSet == self._nbi3gcom_codeSet:
                self.status = STATUS.PASS
            else:
                self.status = STATUS.FAIL
                self.IMPACT.append("nbi3gc can not work normally")
                self.RCA.append("codeset are not match between nbi3gc and nbi3gcom")
                self.RCA.append("nbi3gc codeset is %s"%self._nbi3gc_codeSet)
                self.RCA.append("nbi3gcom codeset is %s"%self._nbi3gcom_codeSet)
                self.FIXSTEP.append("""reset codeset as below configuration:
                %s:jacorb.native_char_codeset
                %s:jacorb.native_char_codeset
                """%(NBI3GC_MF_JACORB_PROPERTIES,NBI3GCOM_PROPERTIES))
                self.FIXSTEP.append("#smanager.pl stop service nbi3gc")
                self.FIXSTEP.append("#smanager.pl stop service nbi3gcom")
                self.FIXSTEP.append("#smanager.pl start service nbi3gcom")
                self.FIXSTEP.append("#smanager.pl start service nbi3gc")

        else:
            self.status = STATUS.PASS

