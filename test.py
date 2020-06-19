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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import telepot
import webbrowser

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import job#c/c++ 연동

STRX = 750
STRY = 30
STRD = 30
TOTAL = 0
BACKGROUNDCOLOR = '#2d2c34'
FONTCOLOR = 'white'
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
def extractXmlSupportData(strXml):
    tree = ElementTree.fromstring(strXml)
    support = []
    for wanted in tree.findall('jynEmpSptList'):
        busiNm = wanted.find('busiNm').text
        dtlBusiNm = wanted.find('dtlBusiNm').text
        busiSum = wanted.find('busiSum').text
        chargerOrgNm = wanted.find('chargerOrgNm').text
        busiTpCd = wanted.find('busiTpCd').text
        ageEtcCont = wanted.find('ageEtcCont').text
        edubgEtcCont = wanted.find('edubgEtcCont').text
        empEtcCont = wanted.find('empEtcCont').text
        relInfoUrl = wanted.find('relInfoUrl').text
        support.append(Support(busiNm,dtlBusiNm,busiSum,chargerOrgNm,busiTpCd,ageEtcCont,edubgEtcCont,empEtcCont,relInfoUrl))
    return support

def extractXmlOpenData(strXml):
    tree = ElementTree.fromstring(strXml)
    opened = []
    for wanted in tree.findall('dhsOpenEmpInfo'):
        empWantedTitle = wanted.find('empWantedTitle').text
        empBusiNm = wanted.find('empBusiNm').text
        if wanted.find('coClcdNm').text:
            coClcdNm = wanted.find('coClcdNm').text
        else:
            coClcdNm = '일반기업'
        empWantedStdt = wanted.find('empWantedStdt').text
        empWantedEndt = wanted.find('empWantedEndt').text
        empWantedTypeNm = wanted.find('empWantedTypeNm').text
        empWantedHomepgDetail = wanted.find('empWantedHomepgDetail').text
        opened.append(Opens(empWantedTitle,empBusiNm,coClcdNm,empWantedStdt,empWantedEndt,empWantedTypeNm,empWantedHomepgDetail))
    return opened

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
        for i in range(len(self.jobs)):
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

        url = url + "center=" + center + "&zoom=" + str(self.mapzoom) + "&size=280x500"+'&markers=size:middle%7Ccolor:green%7C'+ center +tstr+ "&key="+api_key+"&sensor=true"
        #print(url)
        response = requests.get(url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

        label = Label(self.window, image=img, height=250, width=500)
        label.place(x=STRX, y=STRY + STRD * 15)

        self.mapimage = Label(self.window,image=photo,height=300,width=500)


    def showpiegraph(self):
        beernum = []
        price = []
        for i in range(len(self.bookmarklist)):
            beernum.append(i)
            price.append(job.salcount(int(self.bookmarklist[i].minSal)))

        fig = plt.figure()
        plt.pie(price,labels=beernum,shadow=True,autopct='%1.1f%%')
        '''
        plt.pie(price,
                labels=beernum,
                colors=['r', 'm', 'b', 'c', 'k'],
                startangle=90,
                shadow=True,
                explode=(0, 0.1, 0, 0, 0),
                autopct='%1.1f%%')
        '''
        fig.set_size_inches(7.0, 4.1, forward=True)
        self.cgraph = FigureCanvasTkAgg(fig, master=self.frame2)
        self.cgraph.get_tk_widget().place(x=10, y=360)

    def showbargraph(self):
        fig = plt.figure()

        beernum = []
        price = []
        for i in range(len(self.bookmarklist)):
            beernum.append(i)
            price.append(job.salcount(int(self.bookmarklist[i].minSal)))

        plt.bar(range(len(price)), price)
        ax = plt.subplot()
        ax.set_xlabel('company')
        ax.set_ylabel('money')
        ax.set_xticks(beernum)
        ax.set_xticklabels(beernum,rotation=30)

        fig.set_size_inches(7.0, 4.1, forward=True)
        self.cgraph = FigureCanvasTkAgg(fig, master=self.frame2)
        self.cgraph.get_tk_widget().place(x=10, y=360)

    def showlinegraph(self):
        fig = plt.figure()

        beernum = []
        price = []
        for i in range(len(self.bookmarklist)):
            beernum.append(i)
            price.append(job.salcount(int(self.bookmarklist[i].minSal)))

        plt.plot(beernum, price)
        ax = plt.subplot()
        ax.set_xlabel('company')
        ax.set_ylabel('money')
        ax.set_xticks(beernum)
        ax.set_xticklabels(beernum,rotation=30)

        fig.set_size_inches(7.0, 4.1, forward=True)
        self.cgraph = FigureCanvasTkAgg(fig, master=self.frame2)
        self.cgraph.get_tk_widget().place(x=10, y=360)

    def addbookmark(self):
        self.jobs[self.sindex].bookmarkactive = True
        self.bookmarkb.configure(image=self.onbookphoto)
        self.bookmarklist.append(self.jobs[self.sindex])
        self.bookmarkbox.delete(0, END)
        for i in range(len(self.bookmarklist)):
            self.bookmarkbox.insert(END,'['+str(i)+']'+ self.bookmarklist[i].pirntstrJobs())

    def deletebookmark(self):
        del self.bookmarklist[self.sindex]
        self.bookmarkbox.delete(0, END)
        for i in range(len(self.bookmarklist)):
            self.bookmarkbox.insert(END,'['+str(i)+']'+ self.bookmarklist[i].pirntstrJobs())

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

    def createLabel(self, lframe):
        self.title = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"업무 : "
        self.title.place(x=STRX, y=STRY)

        self.jobCont = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#""
        self.jobCont.place(x=STRX, y=STRY + STRD)

        self.salTpNm = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#""
        self.salTpNm.place(x=STRX, y=STRY + STRD * 2)
        self.holidayTpNm = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"근무형태 : "
        self.holidayTpNm.place(x=STRX, y=STRY + STRD * 3)

        self.regionstr = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"지역 : "
        self.regionstr.place(x=STRX, y=STRY + STRD * 5)
        self.certificate = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"자격증 : "
        self.certificate.place(x=STRX, y=STRY + STRD * 6)
        self.minEdubg = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"학력 : "
        self.minEdubg.place(x=STRX, y=STRY + STRD * 7)
        self.career = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"경력 : "
        self.career.place(x=STRX, y=STRY + STRD * 8)
        self.regDt = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"채용기간 : "
        self.regDt.place(x=STRX, y=STRY + STRD * 9)
        self.rcptMthd = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"접수 방법 : "
        self.rcptMthd.place(x=STRX, y=STRY + STRD * 10)
        self.company = Label(text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"회사명 : "
        self.company.place(x=STRX, y=STRY + STRD * 11)
        self.reperNm = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"대표 : "
        self.reperNm.place(x=STRX, y=STRY + STRD * 12)
        self.indTpCdNm = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"업종 : "
        self.indTpCdNm.place(x=STRX, y=STRY + STRD * 13)
        self.busiCont = Label(lframe, text="", font=self.TempFont,anchor="w",justify=LEFT,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)#"주된 업종 : "
        self.busiCont.place(x=STRX, y=STRY + STRD * 14)

        self.zoomplusphoto = PhotoImage(file=r'zoomplus.png')
        self.zoomminusphoto = PhotoImage(file=r'zoomminus.png')
        self.mapphoto = PhotoImage(file=r'map.png')
        self.satellitemapphoto = PhotoImage(file=r'satellitemap.png')
        self.mapplus = Button(lframe, width=40,height=40, text='확대',image=self.zoomplusphoto,font=self.TempFont, command=lambda: self.mapzoomchange(0),bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.mapplus.place(x=800, y=745)

        self.mapmin = Button(lframe, width=40,height=40, text='축소',image=self.zoomminusphoto,font=self.TempFont, command=lambda: self.mapzoomchange(1),bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.mapmin.place(x=900, y=745)

        self.maproad = Button(lframe, width=40,height=40, text='일반',image=self.mapphoto,font=self.TempFont, command=lambda: self.maptypechange(0),bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.maproad.place(x=1000, y=745)

        self.maphybrid = Button(lframe, width=40,height=40, text='위성',image=self.satellitemapphoto,font=self.TempFont, command=lambda: self.maptypechange(1),bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.maphybrid.place(x=1100, y=745)

    def printLabel(self):
        # self.jobs[index].pintJobs()
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=D&returnType=XML&wantedAuthNo=' +self.tempList[self.sindex].wantedAuthNo + '&infoSvc=VALIDATION')
        self.coplist(text, self.sindex)

        self.company.configure(text="회사명 : " + self.tempList[self.sindex].corpName)
        self.title.configure(text=self.tempList[self.sindex].wantedTitle)
        self.salTpNm.configure(text=self.tempList[self.sindex].salTpNm)
        self.certificate.configure(text="자격증 : " + self.tempList[self.sindex].certificate)
        self.regionstr.configure(text="주소 : " + self.tempList[self.sindex].corpAddr)
        wdstr = (str)(self.tempList[self.sindex].workdayWorkhrCont)
        self.tempList[self.sindex].workdayWorkhrCont = wdstr.strip()
        self.holidayTpNm.configure(text=self.tempList[self.sindex].workdayWorkhrCont)
        self.minEdubg.configure(text="학력 : " + self.tempList[self.sindex].minEdubg)
        self.career.configure(text="경력 : " + self.tempList[self.sindex].career)
        self.regDt.configure(text="채용기간 : " + self.tempList[self.sindex].regDt + "~" + self.tempList[self.sindex].closeDt)
        self.rcptMthd.configure(text="접수 방법 : " + self.tempList[self.sindex].rcptMthd)

        wdstr = (str)(self.tempList[self.sindex].jobCont)
        adstr = wdstr.strip()
        self.tempList[self.sindex].jobCont = adstr[:100]
        self.jobCont.configure(text=self.tempList[self.sindex].jobCont)
        self.reperNm.configure(text="대표 : " + self.tempList[self.sindex].reperNm)
        self.indTpCdNm.configure(text="업종 : " + self.tempList[self.sindex].indTpCdNm)
        self.busiCont.configure(text="주된 업종 : " + self.tempList[self.sindex].busiCont)

        self.showmap()

    def selectlist(self,event):#리스트 목록 선택할때 정보 보여주기
        index = self.listbox.curselection()[0]
        self.sindex = index

        self.tempList = []
        for i in range(len(self.jobs)):
            self.tempList.append(self.jobs[i])
        if self.jobs[self.sindex].bookmarkactive == False:
            self.bookmarkb.configure(image = self.nobookphoto)
        else:
            self.bookmarkb.configure(image=self.onbookphoto)
        self.printLabel()

    def selectlist2(self,event):#리스트 목록 선택할때 정보 보여주기
        index = self.bookmarkbox.curselection()[0]
        self.sindex = index

        self.tempList = []
        for i in range(len(self.bookmarklist)):
            self.tempList.append(self.bookmarklist[i])

        self.printLabel()

    def supportsearch(self):#검색 결과

        text = request('http://openapi.work.go.kr/opi/opi/opia/jynEmpSptListAPI.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&returnType=xml&busiTpcd=PLCYTP01&chargerClcd=G&startPage=1+&display=20')
        self.supports = extractXmlSupportData(text)

        self.supportbox.delete(0, END)
        for i in range(len(self.supports)):
            self.supportbox.insert(END, self.supports[i].pirntstrSupport())

    def printSupport(self):
        self.title.configure(text=self.tempList[self.sindex].busiNm)
        self.jobCont.configure(text='담당기관 : '+self.tempList[self.sindex].chargerOrgNm)
        self.salTpNm.configure(text=self.tempList[self.sindex].dtlBusiNm)

        tstr = (str)(self.tempList[self.sindex].busiSum)
        astr = tstr[:45]
        cstr = ""
        if len(tstr) > 90:
            bstr = tstr[45:90]
            cstr = tstr[90:]
        else:
            bstr = tstr[45:]
            cstr = tstr[90:]
        self.tempList[self.sindex].busiSum = astr + '\n' + bstr + '\n' + cstr
        self.holidayTpNm.configure(text=self.tempList[self.sindex].busiSum)

        self.regionstr.configure(text=self.tempList[self.sindex].busiTpCd)
        self.certificate.configure(text="연령 : " + self.tempList[self.sindex].ageEtcCont)
        self.minEdubg.configure(text="학력 : " + self.tempList[self.sindex].edubgEtcCont)
        self.career.configure(text="취업상태 : " + self.tempList[self.sindex].empEtcCont)
        self.regDt.configure(text="주소 : " + self.tempList[self.sindex].relInfoUrl)
        self.rcptMthd.configure(text="")
        self.company.configure(text="")
        self.reperNm.configure(text="")
        self.indTpCdNm.configure(text="")
        self.busiCont.configure(text="")

        '''
        wdstr = (str)(self.tempList[self.sindex].jobCont)
        adstr = wdstr.strip()
        self.tempList[self.sindex].jobCont = adstr[:100]
        self.indTpCdNm.configure(text="")
        self.busiCont.configure(text="")
        '''
    def selectlist3(self,event):#리스트 목록 선택할때 정보 보여주기
        index = self.supportbox.curselection()[0]
        self.sindex = index

        self.tempList = []
        for i in range(len(self.supports)):
            self.tempList.append(self.supports[i])

        self.printSupport()

    def opensearch(self):#검색 결과

        text = request('http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=15')
        self.opens = extractXmlOpenData(text)

        self.openbox.delete(0, END)
        for i in range(len(self.opens)):
            self.openbox.insert(END, self.opens[i].pirntstrOpen())

    def printOpen(self):
        self.title.configure(text=self.tempList[self.sindex].empWantedTitle)
        self.jobCont.configure(text='기업명 : '+self.tempList[self.sindex].empBusiNm)
        self.salTpNm.configure(text='기업형태 : '+self.tempList[self.sindex].coClcdNm)

        self.holidayTpNm.configure(text='모집기간 : '+self.tempList[self.sindex].empWantedStdt +'~'+self.tempList[self.sindex].empWantedEndt)

        self.regionstr.configure(text='고용형태 : '+self.tempList[self.sindex].empWantedTypeNm)
        self.certificate.configure(text="")
        self.minEdubg.configure(text="")
        self.career.configure(text="")
        self.regDt.configure(text="")
        self.rcptMthd.configure(text="")
        self.company.configure(text="")
        self.reperNm.configure(text="")
        self.indTpCdNm.configure(text="")
        self.busiCont.configure(text="")

    def selectlist4(self,event):#리스트 목록 선택할때 정보 보여주기
        index = self.openbox.curselection()[0]
        self.sindex = index

        self.tempList = []
        for i in range(len(self.opens)):
            self.tempList.append(self.opens[i])

        self.printOpen()

    def openweb(self):
        webbrowser.open_new(str(self.supports[self.sindex].relInfoUrl))
    def openweb2(self):
        webbrowser.open_new(str(self.opens[self.sindex].empWantedHomepgDetail))
    def strJobinfo(self,index):
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=D&returnType=XML&wantedAuthNo=' +self.tempList[index].wantedAuthNo + '&infoSvc=VALIDATION')
        self.coplist(text, index)
        wdstr = (str)(self.tempList[index].workdayWorkhrCont)
        self.tempList[index].workdayWorkhrCont = wdstr.strip()
        resultstr = (self.tempList[index].wantedTitle+'\n'\
        +self.tempList[index].jobCont+'\n'
        +self.tempList[index].salTpNm+'\n'
        +self.tempList[index].workdayWorkhrCont + '\n'
        +"주소 : " + self.tempList[index].corpAddr+'\n'
        +"자격증 : " + self.tempList[index].certificate + '\n'
        +"학력 : " + self.tempList[index].minEdubg+'\n'
        +"경력 : " + self.tempList[index].career+'\n'
        +"채용기간 : " + self.tempList[index].regDt + "~" + self.tempList[index].closeDt+'\n'
        +"접수 방법 : " + self.tempList[index].rcptMthd+'\n'
        +"회사명 : " + self.tempList[index].corpName + '\n'
        +"대표 : " + self.tempList[index].reperNm+'\n'
        +"업종 : " + self.tempList[index].indTpCdNm+'\n'
        +"주된 업종 : " + self.tempList[index].busiCont+'\n'
        +"=============================================="+'\n')
        return resultstr

    def sendmail(self):
        # 지메일 아이디,비번 입력하기
        email_user = Entry.get(self.eidentry)+'@gmail.com'  # <ID> 본인 계정 아이디 입력
        email_password = Entry.get(self.epwentry)  # <PASSWORD> 본인 계정 암호 입력
        email_send = email_user  # <받는곳주소> 수신자 이메일 abc@abc.com 형태로 입력

        # 제목 입력
        subject = '직업정보 목록입니다. '

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject
        body = ''
        # 본문 내용 입력
        self.tempList = []
        for i in range(len(self.bookmarklist)):
            self.tempList.append(self.bookmarklist[i])
        for i in range(len(self.bookmarklist)):
            body += self.strJobinfo(i)
        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        server.quit()

    def telerstr(self,regionstr):

        rstr = "&region=" + str(regionstr)

        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=10' + rstr)
        rjobs = extractXmlData(text)

        return rjobs

    def telekstr(self, kstr):

        tstr = urllib.parse.quote(kstr)
        rstr = '&keyword='+tstr
        text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=10' + rstr)
        print(text)
        rjobs = extractXmlData(text)

        return rjobs

    def teleSupport(self):

        text = request('http://openapi.work.go.kr/opi/opi/opia/jynEmpSptListAPI.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&returnType=xml&busiTpcd=PLCYTP01&chargerClcd=G&startPage=1+&display=20')
        rsupports = extractXmlSupportData(text)

        return rsupports

    def teleOpen(self):

        text = request('http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=10')
        rsupports = extractXmlOpenData(text)

        return rsupports

    def handler_telegrame(self,msg):
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
        if content_type == 'text':
            str_message = msg['text']
            if str_message[0:1] == '/':
                args = str_message.split(" ")
                command = args[0]
                del args[0]

                if command == '/도움말':
                    self.bot.sendMessage(chat_id,"안녕하세요")
                    self.bot.sendMessage(chat_id, "명령어는 /검색, /지역, /지원정보, /공채 있습니다.")
                elif command == '/검색':
                    w = " ".join(args)
                    teljobs = self.telekstr(w)
                    for i in range(len(teljobs)):
                        self.bot.sendMessage(chat_id,teljobs[i].TeleprintJobs())
                elif command == '/지역':
                    w = " ".join(args)
                    cd = 0
                    if w == '서울':
                        cd = 11000
                    elif w == '인천':
                        cd = 28000
                    elif w == '부산':
                        cd = 26000
                    elif w == '경기':
                        cd = 41000
                    elif w == '대구':
                        cd = 27000
                    elif w == '광주':
                        cd = 29000
                    elif w == '대전':
                        cd = 30000
                    elif w == '울산':
                        cd = 31000
                    elif w == '세종':
                        cd = 36110
                    elif w == '강원':
                        cd = 42000
                    elif w == '충북':
                        cd = 43000
                    elif w == '충남':
                        cd = 44000
                    elif w == '전북':
                        cd = 45000
                    elif w == '전남':
                        cd = 46000
                    elif w == '경북':
                        cd = 47000
                    elif w == '경남':
                        cd = 48000
                    elif w == '제주':
                        cd = 50000
                    teljobs = self.telerstr(cd)
                    for i in range(len(teljobs)):
                        self.bot.sendMessage(chat_id,teljobs[i].TeleprintJobs())

                elif command == '/지원정보':
                    telSupports = self.teleSupport()
                    for i in range(len(telSupports)):
                        self.bot.sendMessage(chat_id,telSupports[i].TeleprintSupport())

                elif command == '/공채':
                    telOpens = self.teleOpen()
                    for i in range(len(telOpens)):
                        self.bot.sendMessage(chat_id,telOpens[i].TeleprintOpen())



    def start_telegramid(self):
        self.bot = telepot.Bot('1182268570:AAF5jJLOx3t-EBUS2hB1Jqz7WJm2cfyyGwM')
        self.bot.message_loop(self.handler_telegrame)

    def __init__(self):
        self.window = Tk()
        self.window.title("텀프로젝트")
        self.window.geometry("1280x800")
        self.window.resizable(False,False)

        self.window.configure(background=BACKGROUNDCOLOR)

        self.TempFont = font.Font(size=10, weight='bold', family='Consolas')

        self.bookmarklist = []
        self.tempList = []
        self.mapzoom = 18
        self.maptype = 0

        noteStyler = ttk.Style()
        noteStyler.element_create('Plain.Notebook.tab', "from", 'default')
        # Redefine the TNotebook Tab layout to use the new element

        noteStyler.layout("TNotebook.Tab",
                          [('Plain.Notebook.tab', {'children':
                                                       [('Notebook.padding', {'side': 'top', 'children':
                                                           [('Notebook.focus', {'side': 'top', 'children':
                                                               [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                                                'sticky': 'nswe'})],
                                                                              'sticky': 'nswe'})],
                                                   'sticky': 'nswe'})])

        noteStyler.configure("TNotebook", background='black', borderwidth=0)
        noteStyler.configure("TNotebook.Tab", background=BACKGROUNDCOLOR, foreground=BACKGROUNDCOLOR, lightcolor=BACKGROUNDCOLOR, borderwidth=0,tabbackground='dark',backdrop='dark')
        noteStyler.configure("TFrame", background='black', foreground='white', borderwidth=0)


        self.notebook = tkinter.ttk.Notebook(self.window,width = 730, height = 800,style='TNotebook.Tab')
        self.notebook.place(x=0,y=0)

        self.frame1 = tkinter.Frame(self.window,background=BACKGROUNDCOLOR)
        self.notebook.add(self.frame1, text='채용 검색')

        self.ldescrpit = Label(self.frame1, text="희망하는 근무 지역과 키워드 검색을 통해 원하는 일자리를 찾을 수 있습니다. ", font=self.TempFont, bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.ldescrpit.place(x=10, y=10)

        self.ldescrpit2 = Label(self.frame1, text="검색결과 리스트 ", font=self.TempFont,
                               bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.ldescrpit2.place(x=10, y=160)

        self.lrsearh = Label(self.frame1,text="근무 희망 지역 ",font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.lrsearh.place(x=10, y=70)

        self.text = request('http://openapi.work.go.kr/opi/commonCode/commonCode.do?returnType=XML&target=CMCD&authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&dtlGb=1')
        self.region = extractXmlRegionData(self.text)
        comboregion = []
        for i in self.region:
            comboregion.append(i.regionNm)
        self.combo = ttk.Combobox(self.frame1, width=20, textvariable=str ,values=comboregion)
        self.combo.place(x=120, y=70)
        self.combo.current(0)

        self.combo2 = ttk.Combobox(self.frame1, width=20, textvariable=str,values='전체')
        self.combo2.place(x=320, y=70)
        self.combo2.current(0)

        self.combo.bind("<<ComboboxSelected>>", self.callbackFunc)

        self.lksearh = Label(self.frame1,text="키워드 ",font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.lksearh.place(x=40, y=110)

        self.kentry = Entry(self.frame1,width=30)
        self.kentry.place(x=120, y=110)

        self.jobserachphoto = PhotoImage(file=r'jobserach.png')
        self.btn = Button(self.frame1, width=60,height=60, text='검색',image=self.jobserachphoto, command=lambda : self.rsearch(0),bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.btn.place(x=500, y=70)

        self.listbox = Listbox(self.frame1,selectmode = 'single',width=100, height = 30)
        self.listbox.place(x=10,y=190)

        self.listbox.bind("<<ListboxSelect>>", self.selectlist)

        self.lpage = Label(text="[ 0 / 0 ]",font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.lpage.place(x=300, y=720)


        self.bright = Button(self.frame1, width=3, text='>', command=lambda : self.rsearch(1),font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bright.place(x=450, y=695)

        self.bleft = Button(self.frame1, width=3, text='<', command=lambda : self.rsearch(2),font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bleft.place(x=200, y=695)

        self.nobookphoto = PhotoImage(file = r'non_bookmark.png')
        self.onbookphoto = PhotoImage(file=r'on_bookmark.png')
        self.bookmarkb = Button(self.frame1, width=50,height=59, text='북마크',image=self.nobookphoto, command=self.addbookmark,font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bookmarkb.place(x=650, y=680)

        self.createLabel(self.window)

        self.frame2 = tkinter.Frame(self.window,background=BACKGROUNDCOLOR)
        self.notebook.add(self.frame2, text="북마크")

        self.lbookdescrpit = Label(self.frame2, text="북마크 리스트", font=self.TempFont,bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.lbookdescrpit.place(x=10, y=10)

        self.bookmarkbox = Listbox(self.frame2,selectmode = 'single',width=100, height = 15)
        self.bookmarkbox.place(x=10,y=35)
        self.bookmarkbox.bind("<<ListboxSelect>>", self.selectlist2)

        self.bookmarkdeletephoto = PhotoImage(file=r'bookmarkdelete.png')
        self.mailphoto = PhotoImage(file=r'mail.png')
        self.piegraphphoto = PhotoImage(file=r'piegraph.png')
        self.bargraphphoto = PhotoImage(file=r'bargraph.png')
        self.linegraphphoto = PhotoImage(file=r'linegraph.png')

        self.bookmarkdeleb = Button(self.frame2, width=40,height=53, text='북마크제거',image=self.bookmarkdeletephoto, command=self.deletebookmark,font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bookmarkdeleb.place(x=670, y=282)

        self.eidL = tkinter.Label(self.frame2, text="구글 아이디",font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.eidL.place(x=10, y=300)
        self.eidentry = Entry(self.frame2,width=20)
        self.eidentry.place(x=110, y=300)

        self.epwL = tkinter.Label(self.frame2, text="구글 비밀번호",font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.epwL.place(x=10, y=330)
        self.epwentry = Entry(self.frame2,width=20,show="*")
        self.epwentry.place(x=110, y=330)
        self.bmail = Button(self.frame2, width=50,height=50, text='메일보내기',image=self.mailphoto, command=self.sendmail,font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bmail.place(x=270, y=298)

        self.bcirclegraph = Button(self.frame2, width=50,height=50, text='원그래프',image=self.piegraphphoto, command=self.showpiegraph,font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bcirclegraph.place(x=380, y=298)
        self.bstickgraph = Button(self.frame2, width=50,height=50, text='막대그래프',image=self.bargraphphoto, command=self.showbargraph,font=self.TempFont,bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.bstickgraph.place(x=480, y=298)
        self.blinegraph = Button(self.frame2, width=50, height=50, text='꺾은선그래프', image=self.linegraphphoto, command=self.showlinegraph, font=self.TempFont, bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.blinegraph.place(x=580, y=298)

        self.frame3 = tkinter.Frame(self.window,background=BACKGROUNDCOLOR)
        self.notebook.add(self.frame3, text="청년 취업 정보")

        self.lsupportdescrpit = Label(self.frame3, text="청년 취업 지원 정보를 알려줍니다.", font=self.TempFont, bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.lsupportdescrpit.place(x=10, y=10)

        self.lopendescrpit = Label(self.frame3, text="공채 정보를 알려줍니다.", font=self.TempFont, bg=BACKGROUNDCOLOR,fg=FONTCOLOR)
        self.lopendescrpit.place(x=10, y=360)

        self.webenterphoto = PhotoImage(file=r'webenter.png')
        self.supportsearchphoto = PhotoImage(file=r'supportsearch.png')

        self.sbtn = Button(self.frame3, width=40,height=40, text='검색',image=self.supportsearchphoto, command=self.supportsearch, font=self.TempFont,bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.sbtn.place(x=670,y=0)

        self.webbtn = Button(self.frame3, width=40,height=40, text='열기',image=self.webenterphoto, command=self.openweb, font=self.TempFont,bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.webbtn.place(x=670,y=295)

        self.supportbox = Listbox(self.frame3,selectmode = 'single',width=100, height = 15)
        self.supportbox.place(x=10,y=50)
        self.supportbox.bind("<<ListboxSelect>>", self.selectlist3)

        self.openbtn = Button(self.frame3, width=40, height=40, text='검색', image=self.supportsearchphoto,command=self.opensearch, font=self.TempFont, bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.openbtn.place(x=670, y=355)

        self.webbtn2 = Button(self.frame3, width=40, height=40, text='열기', image=self.webenterphoto,command=self.openweb2, font=self.TempFont, bg=BACKGROUNDCOLOR, fg=FONTCOLOR)
        self.webbtn2.place(x=670, y=648)

        self.openbox = Listbox(self.frame3, selectmode='single', width=100, height=15)
        self.openbox.place(x=10, y=400)
        self.openbox.bind("<<ListboxSelect>>", self.selectlist4)

        self.start_telegramid()
        self.window.mainloop()
JobsTk()