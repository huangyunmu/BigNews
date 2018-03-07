# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from urllib import request
from bs4 import BeautifulSoup as bs
from API import APISet
from Util import DataLoader

import datetime
import threading
import time
import json
# install beautifulsoup4 is necessary

    
def getsohunews(path):
    inlist=[]
    t=[]
    path = 'sohu'+path+'.json'
    
    try:
        data = open(path,'r')
        for line in data:
            t.append(json.loads(line)['title'])
        #t.append(line.split('\t')[0])
            
        print(t)
        data.close()
    except IOError:
        data = open(path,'w')
        data.close()
    
    resp = request.urlopen('https://www.sohu.com/')
    html_data = resp.read().decode('utf-8')
    #print(html_data)
    #First box
    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',attrs={'class':'news'})
    slist = temp[0].find_all('a')
    for item in slist:
        if len(item.attrs['title']) < 5:
            break
        if t.count(item.attrs['title']) == 0:
            #print('new news')
            print(item.attrs['title'])
            title = item.attrs['title']
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                print(result['content'])
                content = result['content']
            
            #print(item.attrs['title'])
            #print(content)
            #newresult = APISet.TextKeywords.getKeyword(title,content)
            #print(newresult)
            tempdiction = {}
            '''
            if(result != None):
                for something in result:       
                    tempdiction['keyword']=[]
                    tempdiction['score']=[]
                    try:
                        tempdiction['keyword'].append(something['keyword'])
                        print(something['keyword'])
                    except TypeError:
                        tempdiction['keyword'].append("null")

                    try:
                        tempdiction['score'].append(something['score'])
                    except TypeError:
                        tempdiction['score'].append("null")
                    '''
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            inlist.append(tempdiction)
        else:print('already exist')
    #Second box
    temp = soup.find_all('div',attrs={'class':'list-mod list-mod-1'})
    slist = temp[0].find_all('a')
    for item in slist:
        if t.count(item.attrs['title']) == 0:
            title = item.attrs['title']
            print('new news')
            content = title
            #print(content)
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                #print(result['content'])
                content = result['content']
            tempdiction = {}
            '''
            if(result != None):
                for something in result:
                    
                    tempdiction['keyword']=[]
                    tempdiction['score']=[]
                    try:
                        tempdiction['keyword'].append(something['keyword'])
                    except TypeError:
                        tempdiction['keyword'].append("null")
                    try:
                        tempdiction['score'].append(something['score'])
                    except TypeError:
                        tempdiction['score'].append("null")
            '''         
            tempdiction['title']=title
            tempdiction['content']=content
            tempdiction['jump']=item.attrs['href']
            inlist.append(tempdiction)
        else:
            print('already exist')
    with open(path,'a') as outfile:
        for i in range(0, len(inlist)):
            json.dump(inlist[i],outfile,ensure_ascii=False)
            outfile.write('\n')
    outfile.close()
#    fi = open(path, 'a')
#    for i in range(0, len(inlist)):
#        print(inlist[i]['title']+' '+inlist[i]['jump']+inlist[i]['keyword']+inlist[i]['score'])
#        #fi.write(inlist[i]['title']+' '+inlist[i]['jump']+inlist[i]['keyword']+inlist[i]['score'])
#    fi.close()
    

def getsinanews(path):
    inlist=[]
    t=[]
    path = 'sina'+path+'.json'
    
    try:
        data = open(path,'r')
        for line in data:
            t.append(json.loads(line)['title'])
        data.close()
    except IOError:
        data = open(path,'w')
        data.close()
    
    resp = request.urlopen('https://www.sina.com.cn/')
    html_data = resp.read().decode('utf-8')
    #First box
    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',id='newslist_a')
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        print(item.string)
        if (len(item.string) > 5) & (t.count(item.string) == 0):
            #print('new news')
            print(item.string)
            title = item.string
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                print(result['content'])
                content = result['content']
            
            #print(item.attrs['title'])
            #print(content)
            #newresult = APISet.TextKeywords.getKeyword(title,content)
            #print(newresult)
            tempdiction = {}

            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            inlist.append(tempdiction)
        else:print('already exist')
   
    with open(path,'a') as outfile:
        for i in range(0, len(inlist)):
            json.dump(inlist[i],outfile,ensure_ascii=False)
            outfile.write('\n')
    outfile.close()




    

    #for item in slist:
def gettencentnews(path):
    inlist=[]
    t=[]
    path = 'tencent'+path+'.json'
    
    try:
        data = open(path,'r')
        for line in data:
            t.append(json.loads(line)['title'])
        data.close()
    except IOError:
        data = open(path,'w')
        data.close()
    
    resp = request.urlopen('https://news.qq.com/')
    print(resp)
    html_data = resp.read().decode('utf-8')
    print(html_data)
    #First box
    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',attrs={'bosszone':'ws_tt'})
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        print(item.string)
        if (len(item.string) > 5) & (t.count(item.string) == 0):
            #print('new news')
            print(item.string)
            title = item.string
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                print(result['content'])
                content = result['content']
            
            #print(item.attrs['title'])
            #print(content)
            #newresult = APISet.TextKeywords.getKeyword(title,content)
            #print(newresult)
            tempdiction = {}

            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            inlist.append(tempdiction)
        else:print('already exist')
   
    with open(path,'a') as outfile:
        for i in range(0, len(inlist)):
            json.dump(inlist[i],outfile,ensure_ascii=False)
            outfile.write('\n')
    outfile.close()

    
def getnetnews(path):
    inlist=[]
    t=[]
    path = 'net'+path+'.json'
    
    try:
        data = open(path,'r')
        for line in data:
            t.append(json.loads(line)['title'])
        data.close()
    except IOError:
        data = open(path,'w')
        data.close()
    
    resp = request.urlopen('http://www.163.com/')
    html_data = resp.read().decode('gbk','ignore')
    #print(html_data)
    #First box
    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',attrs={'class':'yaowen_news'})
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        #print(item.string)
        if (len(item.string) > 5) & (t.count(item.string) == 0):
            #print('new news')
            print(item.string)
            title = item.string
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                print(result['content'])
                content = result['content']
    
            tempdiction = {}
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            inlist.append(tempdiction)
        else:print('already exist')
   
    with open(path,'a') as outfile:
        for i in range(0, len(inlist)):
            json.dump(inlist[i],outfile,ensure_ascii=False)
            outfile.write('\n')
    outfile.close()
#def getfenghuangnews():
#def getxinhuanews():
#def getsinanews()


#this is begining of main function
lastday = datetime.datetime.now().day

date = str(datetime.datetime.now().month) + str(lastday)

#getsohunews(date)
#getsinanews(date)
#gettencentnews(date) #Something wrong here
getnetnews(date)






