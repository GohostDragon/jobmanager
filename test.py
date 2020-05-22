#-*- coding:utf-8 -*-

from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import urllib.request

def extractXmlData(strXml): #strXml은 OpenAPI 검색 결과 XML 문자열
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
   # print (strXml)
    # Book 엘리먼트를 가져옵니다.
    for wanted in tree.findall('wanted'):
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


        print("회사명:",company)
        print("업무:", title)
        print(salTpNm,":",sal)
        print("최저연봉:", minSal)
        print("최대연봉:", maxSal)
        print("지역:", region)
        print("근무형태:", holidayTpNm)
        print("학력:", minEdubg)
        print("경력:", career)
        print("등록일시:", regDt)
        print('마감일시:', closeDt)
        print("상세 사이트:",wantedInfoUrl)
        print('===========================')
    return {"company": company, "title": title}

def request(url):
    """지정한 url의 웹 문서를 요청하여, 본문을 반환한다."""
    response = urllib.request.urlopen(url)
    byte_data = response.read()
    text_data = byte_data.decode('utf-8')
    return text_data

text = request('http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKAHJXAWPT27BR8CVH0M2VR1HK&callTp=L&returnType=XML&startPage=1&display=10')
print (text)
extractXmlData(text)

'''
window = Tk()
window.title("텀프로젝트")
window.geometry("800x600")
window.resizable(False,False)

TempFont = font.Font(size=16, weight='bold', family='Consolas')

label = []
entry = []

notebook = tkinter.ttk.Notebook(window,width = 400, height = 600)
notebook.place(x=400,y=0)

frame1 = tkinter.Frame(window)
notebook.add(frame1, text='페이지1')

label1 = tkinter.Label(frame1, text="페이지 1의 내용")
label1.pack()

frame2 = tkinter.Frame(window)
notebook.add(frame2, text="페이지2")

label2 = tkinter.Label(frame2, text="페이지 2의 내용")
label2.pack()

frame3 = tkinter.Frame(window)
notebook.add(frame3, text="페이지4")

label3 = tkinter.Label(frame3, text="페이지 4의 내용")
label3.pack()

# insert(tabname, frame, option) : 텝 메뉴의 tabname 위치에 페이지를 추가
# tabname : index로 사용하거나, frame 위젯의 변수 이름으로 사용
frame4 = tkinter.Frame(window)
notebook.insert(2, frame4, text="페이지3")

label4 = tkinter.Label(frame4, text="페이지3의 내용")
label4.pack()

# enable_traversal() : 탭 메뉴의 키 바인딩을 허용
notebook.enable_traversal()


window.mainloop()
'''