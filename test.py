#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import font

from tkinter import ttk
import tkinter.messagebox
import urllib.request
from xml.etree import ElementTree

from Jobs import *
from Region import *

STRX = 750
STRY = 30
STRD = 20

def extractXmlData(strXml): #strXml은 OpenAPI 검색 결과 XML 문자열
    tree = ElementTree.fromstring(strXml)
    jobs = []
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

def extractXmlRegionData(strXml): #strXml은 OpenAPI 검색 결과 XML 문자열
    tree = ElementTree.fromstring(strXml)
    regions = []
    for wanted in tree.findall('oneDepth'):
        regionCd = wanted.find('regionCd').text
        regionNm = wanted.find('regionNm').text

        regions.append(Region(regionCd,regionNm))
    return regions

def request(url):
    """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
    response = urllib.request.urlopen(url)
    byte_data = response.read()
    text_data = byte_data.decode('utf-8')
    return text_data

class JobsTk:
    def callbackFunc(self,event):
        print("New Element Selected")
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

    def rsearch(self):
        rstr = ""
        if(self.combo.current() == 0):
            rstr = ""
        else:
            rstr = "&region=" + self.dregions[self.combo2.current()].regionCd
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=10'+rstr)
        self.jobs = extractXmlData(text)

        self.listbox.delete(0, END)
        for i in range(10):
            self.listbox.insert(END, self.jobs[i].pirntstrJobs())

    def selectlist(self,event):
        index = self.listbox.curselection()[0]
        self.jobs[index].pintJobs()
        self.company.configure(text="회사명 : " + self.jobs[index].company)
        self.title.configure(text="업무 : " + self.jobs[index].title)
        self.salTpNm.configure(text=self.jobs[index].salTpNm + " : " + self.jobs[index].sal)
        self.minSal .configure(text="최저급 : " + self.jobs[index].minSal)
        self.maxSal.configure(text="최대급 : " + self.jobs[index].maxSal)
        self.regionstr.configure(text="지역 : " + self.jobs[index].region)
        self.holidayTpNm.configure(text="근무형태 : " + self.jobs[index].holidayTpNm)
        self.minEdubg.configure(text="학력 : " + self.jobs[index].minEdubg)
        self.career.configure(text="경력 : " + self.jobs[index].career)
        self.regDt.configure(text="등록일시 : " + self.jobs[index].regDt)
        self.closeDt.configure(text="마감일시 : " + self.jobs[index].closeDt)
        self.wantedInfoUrl.configure(text="상세 사이트 : " + self.jobs[index].wantedInfoUrl)
    def __init__(self):
        self.window = Tk()
        self.window.title("텀프로젝트")
        self.window.geometry("1280x800")
        self.window.resizable(False,False)

        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        self.label = []
        self.entry = []

        self.text = request('http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&dtlGb=1')
        self.region = extractXmlRegionData(self.text)
        comboregion = []
        for i in self.region:
            comboregion.append(i.regionNm)
        self.combo = ttk.Combobox(self.window, width=20, textvariable=str ,values=comboregion)
        self.combo.grid(column = 0 , row = 0)
        self.combo.current(0)

        self.combo2 = ttk.Combobox(self.window, width=20, textvariable=str,values='전체')
        self.combo2.grid(column = 1 , row = 0)
        self.combo2.current(0)

        self.combo.bind("<<ComboboxSelected>>", self.callbackFunc)


        self.btn = Button(self.window, width=10, text='click', command=self.rsearch)
        self.btn.grid(column=2, row=0)

        self.listbox = Listbox(self.window,selectmode = 'single',width=100, height = 10)
        self.listbox.place(x=0,y=30)

        self.listbox.bind("<<ListboxSelect>>",self.selectlist)

        self.company = Label(text="회사명 : ")
        self.company.place(x=STRX, y=STRY)

        self.title = Label(text="업무 : ")
        self.title.place(x=STRX, y=STRY+STRD)
        self.salTpNm = Label(text="")
        self.salTpNm.place(x=STRX, y=STRY+STRD*2)
        self.minSal = Label(text="최저급 : ")
        self.minSal.place(x=STRX, y=STRY+STRD*3)
        self.maxSal = Label(text="최대급 : ")
        self.maxSal.place(x=STRX, y=STRY+STRD*4)
        self.regionstr = Label(text="지역 : ")
        self.regionstr.place(x=STRX, y=STRY+STRD*5)
        self.holidayTpNm = Label(text="근무형태 : ")
        self.holidayTpNm.place(x=STRX, y=STRY+STRD*6)
        self.minEdubg = Label(text="학력 : ")
        self.minEdubg.place(x=STRX, y=STRY+STRD*7)
        self.career = Label(text="경력 : ")
        self.career.place(x=STRX, y=STRY+STRD*8)
        self.regDt = Label(text="등록일시 : ")
        self.regDt.place(x=STRX, y=STRY+STRD*9)
        self.closeDt = Label(text="마감일시 : ")
        self.closeDt.place(x=STRX, y=STRY+STRD*10)
        self.wantedInfoUrl = Label(text="상세 사이트 : ")
        self.wantedInfoUrl.place(x=STRX, y=STRY+STRD*11)

        '''
        self.notebook = tkinter.ttk.Notebook(self.window,width = 400, height = 600)
        self.notebook.place(x=400,y=0)

        self.frame1 = tkinter.Frame(self.window)
        self.notebook.add(self.frame1, text='페이지1')

        self.label1 = tkinter.Label(self.frame1, text="페이지 1의 내용")
        self.label1.pack()

        self.frame2 = tkinter.Frame(self.window)
        self.notebook.add(self.frame2, text="페이지2")

        self.label2 = tkinter.Label(self.frame2, text="페이지 2의 내용")
        self.label2.pack()

        self.frame3 = tkinter.Frame(self.window)
        self.notebook.add(self.frame3, text="페이지4")

        self.label3 = tkinter.Label(self.frame3, text="페이지 4의 내용")
        self.label3.pack()

        # insert(tabname, frame, option) : 텝 메뉴의 tabname 위치에 페이지를 추가
        # tabname : index로 사용하거나, frame 위젯의 변수 이름으로 사용
        self.frame4 = tkinter.Frame(self.window)
        self.notebook.insert(2, self.frame4, text="페이지3")

        self.label4 = tkinter.Label(self.frame4, text="페이지3의 내용")
        self.label4.pack()

        # enable_traversal() : 탭 메뉴의 키 바인딩을 허용
        self.notebook.enable_traversal()
        '''

        self.window.mainloop()
JobsTk()