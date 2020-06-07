class Region:
    def __init__(self, regionCd,regionNm):
        self.regionCd = regionCd
        self.regionNm = regionNm

class Support:
    def __init__(self,busiNm,dtlBusiNm,busiSum,chargerOrgNm,busiTpCd,ageEtcCont,edubgEtcCont,empEtcCont,relInfoUrl):
        self.busiNm = busiNm
        self.dtlBusiNm = dtlBusiNm
        self.busiSum = busiSum
        self.chargerOrgNm = chargerOrgNm
        self.busiTpCd = busiTpCd
        self.ageEtcCont = ageEtcCont
        self.edubgEtcCont = edubgEtcCont
        self.empEtcCont = empEtcCont
        self.relInfoUrl = relInfoUrl

    def pirntstrSupport(self):
        return str(self.busiNm)
