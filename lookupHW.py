import requests
from bs4 import BeautifulSoup
import os
import lxml

sid=os.environ['SID']
cid=os.environ['CID']
bir=os.environ['BIR']
def login_homework():
    res = requests.get('http://www.yphs.tp.edu.tw/tea/tu2.aspx')
    soup = BeautifulSoup(res.text, "lxml")
    VIEWSTATE = soup.find(id="__VIEWSTATE")
    VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")
    EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")
    res = requests.post('http://www.yphs.tp.edu.tw/tea/tu2.aspx', allow_redirects=False, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),'chk_id':'學生／家長','tbx_sno':sid,'tbx_sid':cid,'tbx_sbir':bir,'but_login_stud':'登　　入'})
    global cook
    cook = res.cookies['ASP.NET_SessionId']
    return

def lookuphw(x):
    global cook,fw
    try:
        send = requests.get('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook})
        soup = BeautifulSoup(send.text, "lxml")
        VIEWSTATE = soup.find(id="__VIEWSTATE")
        VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")
        EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")
        num = str('')
        if(x<10):
            num = '0'+str(x)
        else:
            num = str(x)
        send = requests.post('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook}, data={'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),('GridViewS$ctl'+num+'$but_vf1'):'詳細內容'})
        soup = BeautifulSoup(send.text, "lxml")
        post_author = str(soup.find(id='Lab_publisher').text)
        post_title = str(soup.find(id='Lab_purport').text)
        post_content = str(soup.find(id='Lab_content').text)
        post_attachment = ''
        if(soup.find(target='_blank')):
            post_attachment=soup.find(target='_blank').get('href')
        if(post_attachment != ''):
            post_content=post_content+'\n\n附件: ' + post_attachment
        send_word = [post_content,post_author,post_title]
        return send_word
    except:
        return ['','','']
        pass

def HW():    
    login_homework()
    return lookuphw(2)
