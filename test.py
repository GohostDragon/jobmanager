#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import font

from tkinter import ttk
import tkinter.messagebox
import urllib
#from urllib.parse import quote
import urllib.request
import requests

from xml.etree import ElementTree

from Jobs import *
from Region import *

from io import BytesIO
from PIL import Image,ImageTk
import io
import math

STRX = 750
STRY = 30
STRD = 30
TOTAL = 0
def extractXmlData(strXml): #채용정보 파싱
    tree = ElementTree.fromstring(strXml)
    jobs = []
    global TOTAL
    TOTAL = (int)(tree.find('total').text)
    for wanted in tree.findall('wanted'):
        wantedAuthNo = wanted.find('wantedAuthNo').text
        company = wanted.find('company').text
        title = wanted.find('title').text
        salTpNm = wanted.find('salTpNm').text
        sal = wanted.find('sal').text
        minSal = wanted.find('minSal').text
        maxSal = wanted.find('maxSal').text
        region = wanted.find('region').text
        holidayTpNm = wanted.find('holidayTpNm').text
        minEdubg = wanted.find('minEdubg').text
        career = wanted.find('career').text
        regDt = wanted.find('regDt').text
        closeDt = wanted.find('closeDt').text

        wantedInfoUrl = wanted.find('wantedInfoUrl').text

        jobs.append(Jobs(wantedAuthNo,company,title,salTpNm,sal,minSal,maxSal,region,holidayTpNm,minEdubg,career,regDt,closeDt,wantedInfoUrl))
    return jobs

def extractXmlRegionData(strXml): #지역 파싱
    tree = ElementTree.fromstring(strXml)
    regions = []
    for wanted in tree.findall('oneDepth'):
        regionCd = wanted.find('regionCd').text
        regionNm = wanted.find('regionNm').text

        regions.append(Region(regionCd,regionNm))
    return regions

def request(url):
    """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
    response = urllib.request.urlopen(url).read().decode('utf-8')
    #byte_data = response.read()
    #text_data = byte_data.decode('utf-8')
    #return text_data
    return response

class JobsTk:
    def callbackFunc(self,event):#지역 검색
        i = self.combo.current()
        sregion = self.region[i].regionCd
        tree = ElementTree.fromstring(self.text)
        self.dregions = []
        self.dregions.append(Region(sregion, '전체'))
        for wanted in tree.findall('oneDepth'):
            if(wanted.find('regionCd').text == sregion):
                for aregion in wanted.findall('twoDepth'):
                    regionCd = aregion.find('regionCd').text
                    regionNm = aregion.find('regionNm').text
                    self.dregions.append(Region(regionCd, regionNm))
        comboregion = []
        for i in self.dregions:
            comboregion.append(i.regionNm)
        self.combo2['value'] = comboregion
        self.combo2.current(0)

    def rsearch(self,type):#검색 결과
        rstr = ""
        if(self.combo.current() == 0):
            rstr = ""
        else:
            rstr = "&region=" + self.dregions[self.combo2.current()].regionCd

        kstr2 = ""
        kstr = Entry.get(self.kentry)
        if kstr != "":
            kstr2 = '&keyword='
            kstr = urllib.parse.quote(kstr)
        global TOTAL
        max_page = TOTAL // 30
        if type == 0:
            self.page = 1
        elif type == 1:
            self.page += 1
            if self.page > max_page:
                self.page = max_page
        else:
            self.page -= 1
            if self.page < 1:
                self.page = 1
        #a = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage='+str(self.page)+'&display=10'+rstr+kstr
        #print(a)
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage='+str(self.page)+'&display=30'+rstr+kstr2+kstr)
        self.jobs = extractXmlData(text)

        self.listbox.delete(0, END)
        for i in range(30):
            self.listbox.insert(END, self.jobs[i].pirntstrJobs())

        self.lpage.configure(text="[" + str(self.page)+'/'+str(max_page)+"]")
    def showmap(self):
        api_key = "AIzaSyDT7sSTMO5sgyqu_1l0KuaIK_QAyv0U44c"
        url = "https://maps.googleapis.com/maps/api/staticmap?"
        t = (str)(self.jobs[self.sindex].corpAddr)
        center = t.replace(" ","")
        if self.maptype == 0:
            tstr = '&maptype=roadmap'
        else:
            tstr = '&maptype=hybrid'

        url = url + "center=" + center + "&zoom=" + str(self.mapzoom) + "&size=300x300"+'&markers=size:middle%7Ccolor:green%7C'+ center +tstr+ "&key="+api_key+"&sensor=true"
        #print(url)
        response = requests.get(url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

        label = Label(self.frame1, image=img, height=300, width=300)
        label.place(x=STRX, y=STRY + STRD * 15)

        self.mapimage = Label(self.frame1,image=photo,height=400,width=400)
    def mapzoomchange(self,type):
        if type == 0:
            self.mapzoom += 1
            if self.mapzoom > 19:
                self.mapzoom = 19
        else:
            self.mapzoom -= 1
            if self.mapzoom < 10:
                self.mapzoom = 10
        self.showmap()

    def maptypechange(self,type):
        if type == 0:
            self.maptype = 0
        else:
            self.maptype = 1
        self.showmap()

    def coplist(self,strxml,index):
        tree = ElementTree.fromstring(strxml)
        corpinfo = tree.find('corpInfo')
        corpNm = corpinfo.find('corpNm').text
        reperNm = corpinfo.find('reperNm').text
        totPsncnt = corpinfo.find('totPsncnt').text
        indTpCdNm = corpinfo.find('indTpCdNm').text
        busiCont = corpinfo.find('busiCont').text
        corpAddr = corpinfo.find('corpAddr').text
        busiSize = corpinfo.find('busiSize').text
        self.jobs[index].addcorp(corpNm, reperNm, totPsncnt, indTpCdNm, busiCont, corpAddr, busiSize)

        wantedinfo = tree.find('wantedInfo')
        jobsNm = wantedinfo.find('jobsNm').text
        wantedTitle = wantedinfo.find('wantedTitle').text
        receiptCloseDt = wantedinfo.find('receiptCloseDt').text
        empTpNm = wantedinfo.find('empTpNm').text
        salTpNm = wantedinfo.find('salTpNm').text
        enterTpNm = wantedinfo.find('enterTpNm').text
        eduNm = wantedinfo.find('eduNm').text
        jobCont = wantedinfo.find('jobCont').text
        if(wantedinfo.find('certificate').text):
            certificate = wantedinfo.find('certificate').text
        else:
            certificate = '관계없음'
        compAbl = wantedinfo.find('compAbl').text
        selMthd = wantedinfo.find('selMthd').text
        rcptMthd = wantedinfo.find('rcptMthd').text
        submitDoc = wantedinfo.find('submitDoc').text
        workdayWorkhrCont = wantedinfo.find('workdayWorkhrCont').text
        self.jobs[index].addcwanted(jobsNm,wantedTitle,receiptCloseDt,empTpNm,salTpNm,enterTpNm,eduNm,certificate,compAbl,selMthd,rcptMthd,submitDoc,workdayWorkhrCont,jobCont)

    def selectlist(self,event):#리스트 목록 선택할때 정보 보여주기
        index = self.listbox.curselection()[0]
        self.sindex = index
        #self.jobs[index].pintJobs()
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=D&returnType=XML&wantedAuthNo='+ self.jobs[index].wantedAuthNo +'&infoSvc=VALIDATION')
        self.coplist(text,index)


        self.company.configure(text="회사명 : " + self.jobs[index].company)
        self.title.configure(text=self.jobs[index].wantedTitle)
        self.salTpNm.configure(text=self.jobs[index].salTpNm)
        self.certificate .configure(text="자격증 : " + self.jobs[index].certificate)
        self.regionstr.configure(text="주소 : " + self.jobs[index].corpAddr)
        wdstr = (str)(self.jobs[index].workdayWorkhrCont)
        self.jobs[index].workdayWorkhrCont = wdstr.strip()
        self.holidayTpNm.configure(text=self.jobs[index].workdayWorkhrCont)
        self.minEdubg.configure(text="학력 : " + self.jobs[index].minEdubg)
        self.career.configure(text="경력 : " + self.jobs[index].career)
        self.regDt.configure(text="채용기간 : " + self.jobs[index].regDt+"~"+ self.jobs[index].closeDt)
        self.rcptMthd.configure(text="접수 방법 : " + self.jobs[index].rcptMthd)

        self.jobCont.configure(text=self.jobs[index].jobCont)
        self.reperNm.configure(text="대표 : " + self.jobs[index].reperNm)
        self.indTpCdNm.configure(text="업종 : " + self.jobs[index].indTpCdNm)
        self.busiCont.configure(text="주된 업종 : " + self.jobs[index].busiCont)

        self.showmap()

    def __init__(self):
        self.window = Tk()
        self.window.title("텀프로젝트")
        self.window.geometry("1280x800")
        self.window.resizable(False,False)

        self.TempFont = font.Font(size=10, weight='bold', family='Consolas')

        self.label = []
        self.mapzoom = 18
        self.maptype = 0

        self.notebook = tkinter.ttk.Notebook(self.window,width = 1280, height = 800)
        self.notebook.place(x=0,y=0)

        self.frame1 = tkinter.Frame(self.window)
        self.notebook.add(self.frame1, text='채용 검색')

        self.lrsearh = Label(self.frame1,text="근무 희망 지역 ",font=self.TempFont)
        self.lrsearh.grid(column = 0 , row = 0)

        self.text = request('http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&dtlGb=1')
        self.region = extractXmlRegionData(self.text)
        comboregion = []
        for i in self.region:
            comboregion.append(i.regionNm)
        self.combo = ttk.Combobox(self.frame1, width=20, textvariable=str ,values=comboregion)
        self.combo.grid(column = 1 , row = 0)
        self.combo.current(0)

        self.combo2 = ttk.Combobox(self.frame1, width=20, textvariable=str,values='전체')
        self.combo2.grid(column = 2 , row = 0)
        self.combo2.current(0)

        self.combo.bind("<<ComboboxSelected>>", self.callbackFunc)

        self.ljsearh = Label(self.frame1,text="희망 직종 ")
        self.ljsearh.grid(column = 0 , row = 1)

        self.lksearh = Label(self.frame1,text="키워드 ",font=self.TempFont)
        self.lksearh.grid(column = 0 , row = 2)

        self.kentry = Entry(self.frame1,width=20)
        self.kentry.grid(column=1, row=2)

        self.btn = Button(self.frame1, width=10, text='검색', command=lambda : self.rsearch(0))
        self.btn.grid(column=3, row=0)

        self.listbox = Listbox(self.frame1,selectmode = 'single',width=100, height = 30)
        self.listbox.place(x=0,y=100)

        self.listbox.bind("<<ListboxSelect>>",self.selectlist)

        self.lpage = Label(text="[ 0 / 0 ]")
        self.lpage.place(x=300, y=620)

        self.bright = Button(self.frame1, width=3, text='>', command=lambda : self.rsearch(1))
        self.bright.place(x=350, y=595)

        self.bleft = Button(self.frame1, width=3, text='<', command=lambda : self.rsearch(2))
        self.bleft.place(x=250, y=595)

        self.title = Label(self.frame1,text="업무 : ",font=self.TempFont)
        self.title.place(x=STRX, y=STRY)

        self.jobCont = Label(self.frame1,text="",font=self.TempFont)
        self.jobCont.place(x=STRX, y=STRY+STRD)

        self.salTpNm = Label(self.frame1,text="",font=self.TempFont)
        self.salTpNm.place(x=STRX, y=STRY+STRD*2)
        self.holidayTpNm = Label(self.frame1,text="근무형태 : ",font=self.TempFont)
        self.holidayTpNm.place(x=STRX, y=STRY+STRD*3)

        self.regionstr = Label(self.frame1,text="지역 : ",font=self.TempFont)
        self.regionstr.place(x=STRX, y=STRY+STRD*5)
        self.certificate = Label(self.frame1,text="자격증 : ",font=self.TempFont)
        self.certificate.place(x=STRX, y=STRY+STRD*6)
        self.minEdubg = Label(self.frame1,text="학력 : ",font=self.TempFont)
        self.minEdubg.place(x=STRX, y=STRY+STRD*7)
        self.career = Label(self.frame1,text="경력 : ",font=self.TempFont)
        self.career.place(x=STRX, y=STRY+STRD*8)
        self.regDt = Label(self.frame1,text="채용기간 : ",font=self.TempFont)
        self.regDt.place(x=STRX, y=STRY+STRD*9)
        self.rcptMthd = Label(self.frame1,text="접수 방법 : ",font=self.TempFont)
        self.rcptMthd.place(x=STRX, y=STRY+STRD*10)
        self.company = Label(text="회사명 : ",font=self.TempFont)
        self.company.place(x=STRX, y=STRY+355)
        self.reperNm = Label(self.frame1,text="대표 : ",font=self.TempFont)
        self.reperNm.place(x=STRX, y=STRY+STRD*12)
        self.indTpCdNm = Label(self.frame1,text="업종 : ",font=self.TempFont)
        self.indTpCdNm.place(x=STRX, y=STRY+STRD*13)
        self.busiCont = Label(self.frame1,text="주된 업종 : ",font=self.TempFont)
        self.busiCont.place(x=STRX, y=STRY+STRD*14)

        self.mapplus = Button(self.frame1, width=3, text='+', command=lambda : self.mapzoomchange(0))
        self.mapplus.place(x=1100, y=600)

        self.mapmin = Button(self.frame1, width=3, text='-', command=lambda : self.mapzoomchange(1))
        self.mapmin.place(x=1100, y=630)

        self.maproad = Button(self.frame1, width=3, text='일반', command=lambda : self.maptypechange(0))
        self.maproad.place(x=1100, y=660)

        self.maphybrid = Button(self.frame1, width=3, text='위성', command=lambda : self.maptypechange(1))
        self.maphybrid.place(x=1100, y=690)

        self.frame2 = tkinter.Frame(self.window)
        self.notebook.add(self.frame2, text="북마크")

        self.label2 = tkinter.Label(self.frame2, text="페이지 2의 내용")
        self.label2.pack()

        self.frame3 = tkinter.Frame(self.window)
        self.notebook.add(self.frame3, text="추가 기능")

        self.label3 = tkinter.Label(self.frame3, text="페이지 4의 내용")
        self.label3.pack()


        self.window.mainloop()
JobsTk()