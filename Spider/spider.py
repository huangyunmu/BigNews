# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from urllib import request
from bs4 import BeautifulSoup as bs
from API import APISet
from Util import DataLoader
from operator import itemgetter
from bosonnlp import BosonNLP

import datetime
import threading
import time
import json
import http.client
import os
import sys


#来源：疯狂的赵凡越
# install beautifulsoup4 is necessary
# install $ pip install -U bosonnlp is necessary

def writeresult(path,inlist):
    os.remove(path)
    #Delete wrong things
    with open('test.json','a') as outfile:
        flag = 0
        while(flag == 0):
            temp = len(inlist)
            for i in range(0, len(inlist)):
                print('This is '+str(i))
                try:
                    json.dump(inlist[i],outfile,ensure_ascii=False)
        
                    if(i == (temp-1)):
                        flag = 1
                except:
                    del inlist[i]
                    break
            
    os.remove('test.json')
    
    with open(path,'a') as outfile:
        outfile.write('[')
        for i in range(0, len(inlist)-1):
            #print(inlist[i])
            json.dump(inlist[i],outfile,ensure_ascii=False)
            outfile.write(',')
        try:
            json.dump(inlist[len(inlist)-1],outfile,ensure_ascii=False)
        except:
            pass
        outfile.write(']')
    outfile.close()
'''
def loadData(path):
    t=[]
    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
            return t
    except IOError:
        data = open(path,'w')
        data.close()
        return t
'''
def getsohunews(path):
    inlist=[]
    t=[]
    path = 'sohu'+path+'.json'

    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path,'w')
        data.close()
    except:
        os.remove(path)
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
        if len(item.attrs['title']) < 8:
            break
        if t.count(item.attrs['title']) == 0:
            #print('new news')
            
            print(item.attrs['title'])
            title = item.attrs['title']
            t.append(title)
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                #print(result['content'])
                content = result['content']    
            
            newtext=content

            tempdiction = {}
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            
            if(len(newtext)>300):
                tempresult = open("tempresult.txt","w")
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        tempresult.write(item['word']+'\t1\n')    
                tempresult.close()
                
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]                
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                    
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                    
                print(readylist)
                tempdiction['keywords']=readylist              
                os.remove("tempresult.txt")
                
            else:
                
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)
                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)

                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist

                print(readylist)
           
            inlist.append(tempdiction)
        else:print('already exist')
    #Second box
    temp = soup.find_all('div',attrs={'class':'list-mod list-mod-1'})
    slist = temp[0].find_all('a')
    for item in slist:
        if t.count(item.attrs['title']) == 0:
            title = item.attrs['title']
            t.append(title)
            print('new news')
            content = title
            print(title)
            result = APISet.ContentGrab.getContent('http:'+item.attrs['href'])
            if(result!=None):
                #print(result['content'])
                content = result['content']
            
            #print(item.attrs['title'])
            #print(content)
            #newresult = APISet.TextKeywords.getKeyword(title,content)
            #print(newresult)
            
            newtext=content

            tempdiction = {}
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            
            if(len(newtext)>300):
                tempresult = open("tempresult.txt","w")
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        tempresult.write(item['word']+'\t1\n')    
                tempresult.close()
                
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]                
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                    
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                    
                print(readylist)
                tempdiction['keywords']=readylist              
                os.remove("tempresult.txt")
                
            else:
                
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)
                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)

                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist

                print(readylist)
            inlist.append(tempdiction)
        else:
            print('already exist')
    writeresult(path,inlist)

def getsinanews(path):
    inlist=[]
    t=[]
    path = 'sina'+path+'.json'
    
    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path,'w')
        data.close()
    except:
        os.remove(path)
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
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            #print('new news')
            print(item.string)
            title = item.string
            t.append(title)
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                #print(result['content'])
                content = result['content']
            
            newtext=content

            tempdiction = {}
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            
            if(len(newtext)>300):
                tempresult = open("tempresult.txt","w")
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        try:
                            tempresult.write(item['word']+'\t1\n')
                        except:
                            pass
                tempresult.close()
                
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]                
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                    
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                    
                print(readylist)
                tempdiction['keywords']=readylist              
                os.remove("tempresult.txt")
                
            else:
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)
                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)

                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist

                print(readylist)
            inlist.append(tempdiction)
            
        else:print('already exist')
   
    writeresult(path,inlist)
    
def getnetnews(path):
    inlist=[]
    t=[]
    path = 'net'+path+'.json'
    
    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path,'w')
        data.close()
    except:
        os.remove(path)
        data = open(path,'w')
        data.close() 
    
    resp = request.urlopen('http://www.163.com/')
    html_data = resp.read().decode('gbk','ignore')

    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',attrs={'class':'yaowen_news'})
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        #print(item.string)
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            #print('new news')
            print(item.string)
            title = item.string
            t.append(title)
            content = title
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                #print(result['content'])
                content = result['content']

            newtext=content
            tempdiction = {}
            tempdiction['title']=title
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            
            if(len(newtext)>300):
                tempresult = open("tempresult.txt","w")
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        try:
                            tempresult.write(item['word']+'\t1\n')
                        except:
                            pass
                tempresult.close()
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]                
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                print(readylist)
                tempdiction['keywords']=readylist
                tempresult.close()
                os.remove("tempresult.txt")
            else:    
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)

                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)
                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist
                print(readylist)
            inlist.append(tempdiction)
            
        else:print('already exist')
    writeresult(path,inlist)

def getfenghuangnews(path):
    inlist=[]
    t=[]
    path = 'fenghuang'+path+'.json'
    
    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                t.append(item['title'])
                inlist.append(item)
    except IOError:
        data = open(path,'w')
        data.close()
    except:
        os.remove(path)
        data = open(path,'w')
        data.close()   
        
    try:
        resp = request.urlopen('http://www.ifeng.com/')
        html_data = resp.read().decode('utf-8','ignore')
    except http.client.IncompleteRead as e:
        html_data = e.partial.decode('utf-8')
    print('successful')

    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',id='headLineDefault')
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        #print(item.string)
        if (item.string == None):
            continue
        if (not((item.attrs['href'][0:10] == 'http://new')|(item.attrs['href'][0:10] == 'https://ne'))):
            continue
        else:
            print(item.attrs['href'])
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            content = item.string
            t.append(item.string)
            #print('new news')
            result = APISet.ContentGrab.getContent(item.attrs['href'])
            if(result!=None):
                content = result['content']
            
            newtext=content

            tempdiction = {}
            tempdiction['title']=item.string
            tempdiction['jump']=item.attrs['href']
            tempdiction['content']=content
            
            if(len(newtext)>300):
                tempresult = open("tempresult.txt","w")
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        try:
                            tempresult.write(item['word']+'\t1\n')
                        except:
                            pass
                tempresult.close()
                
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]                
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                    
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                    
                print(readylist)
                tempdiction['keywords']=readylist              
                os.remove("tempresult.txt")
                
            else:
                
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)
                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)

                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist

                print(readylist)
            inlist.append(tempdiction)            
        else:
            print('already exist')
    writeresult(path,inlist)


def getxinhuanews(path):
    inlist=[]
    t=[]
    path = 'xinhua'+path+'.json'
    
    try:
        with open(path) as f:
            json_str=f.read()
            data=json.loads(json_str)
            for item in data:
                t.append(item['title'])
                inlist.append(item)
    except IOError:
        data = open(path,'w')
        data.close()
    except:
        os.remove(path)
        data = open(path,'w')
        data.close()
    
    resp = request.urlopen('http://www.xinhuanet.com/')
    html_data = resp.read().decode('utf-8','ignore')
    soup = bs(html_data,'html.parser')
    temp = soup.find_all('div',attrs={'class':'borderCont'})
    slist = temp[2].find_all('a')
    print(len(slist))
    for item in slist:
        #print(item.string)
        if (item.string == None):
            break
        if (len(item.string) > 8) & (t.count(item.string) == 0):

            t.append(item.string)
            tempdiction = {}
            tempdiction['title']=item.string
            tempdiction['jump']=item.attrs['href']
               
            content = ''
            temp_data = request.urlopen(item.attrs['href'])
            temphtml = temp_data.read().decode('utf-8','ignore')
            tempsoup = bs(temphtml,'html.parser')
            temptemp = tempsoup.find_all('div',id = 'p-detail')

            try:
                templist = temptemp[0].find_all('p')
            except:
                continue
            try:
                for i in templist:
                    content = content + i.string
            except:
                
                pass
            print(content)
            tempdiction['content']=content
            newtext = content

            tempresult = open("tempresult.txt","w")
            if(len(newtext)<30):
                continue
            if(len(newtext)>300):
                while(len(newtext)>300):
                    text = newtext[0:299]
                    newtext = newtext[300:len(newtext)]
                    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
                    if(combtokens != None):
                        for item in combtokens:
                            tempresult.write(item['word']+'\t1\n')
                combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
                if(combtokens != None):
                    for item in combtokens:
                        try:
                            tempresult.write(item['word']+'\t1\n')
                        except:
                            pass
                tempresult.close()
                
                Dic={}
                for line in open("tempresult.txt"):
                    line = line.strip()
                    word = line.split('\t',1)[0]
                    
                    try:
                        temp = int(1)
                        Dic[word]=Dic.get(word,0)+temp
                    except:
                        pass
                    
                FinalList = sorted(Dic.items(),key = itemgetter(1),reverse = True)
                sumfre = 0
                readylist=[]
                for key,values in FinalList[0:4]:
                    sumfre = sumfre+values
                for key,values in FinalList[0:4]:
                    readylist.append(key)
                    readylist.append(values/sumfre)
                    
                print(readylist)
                tempdiction['keywords']=readylist
                os.remove("tempresult.txt")
                
            else:
                readylist=[]
                sumfre=0
                print("NEW TEXT："+newtext)
                title = newtext
                tempwords=[]

                result = nlp.extract_keywords(newtext,top_k = 4)

                for weight, word in result:
                    sumfre=sumfre+weight
                for weight,word in result:
                    readylist.append(word)
                    readylist.append(weight/sumfre)
                        
                tempdiction['keywords']=readylist

                print(readylist)
            inlist.append(tempdiction)  
                
        
        else:print('already exist')
    writeresult(path,inlist)
def sleeptime(hour,minu,sec):
    return hour*3600+minu*60+sec
#this is begining of main function
lastday = datetime.datetime.now().day
date = str(datetime.datetime.now().month) + str(lastday)
nlp = BosonNLP('4T70m9OU.24533.fXkOVBLkOFVM')
second = sleeptime(0,10,0)
while(1==1):
    getsohunews(date)
    getsinanews(date)
    getnetnews(date)
    getxinhuanews(date)
    getfenghuangnews(date)
    time.sleep(second)






