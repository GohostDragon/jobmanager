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

    def TeleprintSupport(self):
        rstr = (self.busiNm + '\n'
        +'담당기관 : ' + self.chargerOrgNm
        +self.dtlBusiNm+'\n'
        +self.busiSum+'\n'
        +self.busiTpCd+'\n'
        +"연령 : " + self.ageEtcCont+'\n'
        +"학력 : " + self.edubgEtcCont+'\n'
        +"취업상태 : " + self.empEtcCont+'\n'
        +"주소 : " + self.relInfoUrl+'\n')
        return rstr
