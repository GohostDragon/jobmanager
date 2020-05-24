class Jobs:
    def __init__(self, wantedAuthNo,company,title,salTpNm,sal,minSal,maxSal,region,holidayTpNm,minEdubg,career,regDt,closeDt,wantedInfoUrl):
        self.wantedAuthNo = wantedAuthNo
        self.company = company
        self.title = title
        self.salTpNm = salTpNm
        self.sal = sal
        self.minSal = minSal
        self.maxSal = maxSal
        self.region = region
        self.holidayTpNm = holidayTpNm
        self.minEdubg = minEdubg
        self.career = career
        self.regDt = regDt
        self.closeDt = closeDt
        self.wantedInfoUrl = wantedInfoUrl

    def pintJobs(self):
        print("회사명:",self.company)
        print("업무:", self.title)
        print(self.salTpNm,":",self.sal)
        print("최저연봉:", self.minSal)
        print("최대연봉:", self.maxSal)
        print("지역:", self.region)
        print("근무형태:", self.holidayTpNm)
        print("학력:", self.minEdubg)
        print("경력:", self.career)
        print("등록일시:", self.regDt)
        print('마감일시:', self.closeDt)
        print("상세 사이트:",self.wantedInfoUrl)
        print('===========================')

    def pirntstrJobs(self):
        return "["+str(self.region)+"]"+str(self.company)+" "+str(self.salTpNm)+" "+str(self.sal)