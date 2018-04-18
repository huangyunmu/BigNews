# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from urllib import request
from bs4 import BeautifulSoup as bs
from API import APISet
from Util import Util
from operator import itemgetter
from bosonnlp import BosonNLP

import datetime
import threading
import time
import json
import http.client
import os
import sys


# 来源：疯狂的赵凡越
# install beautifulsoup4 is necessary
# install $ pip install -U bosonnlp is necessary
default_top_k=7
def getContentWithRetry(url,retryLimit=3,retryIntervalLimit=8,retryIntervalBegin=2):
    content=None
    retryCount=0
    retryInterval=retryIntervalBegin
    while(retryCount<retryLimit):
        result = APISet.ContentGrab.getContent(url)
        if(result!=None):
#           print(result['content'])
            content = result['content']
            retryInterval=retryIntervalBegin
            break
        else:
            retryCount=retryCount+1
            print("retry: "+str(retryCount)+"for news: "+url)
            if(retryInterval<retryIntervalLimit):
                retryInterval=retryInterval*2
            time.sleep(retryInterval)  
    if(content==None):
        return None
    else:
        return content
def writeresult(path, inlist):
    os.remove(path)
    # Delete wrong things
    with open('test.json', 'a') as outfile:
        flag = 0
        while(flag == 0):
            temp = len(inlist)
            for i in range(0, len(inlist)):
                print('This is ' + str(i))
                try:
                    json.dump(inlist[i], outfile, ensure_ascii=False)
                    if(i == (temp - 1)):
                        flag = 1
                except:
                    del inlist[i]
                    break
    os.remove('test.json')
    
    with open(path, 'a') as outfile:
        outfile.write('[')
        for i in range(0, len(inlist) - 1):
            # print(inlist[i])
            json.dump(inlist[i], outfile, ensure_ascii=False)
            outfile.write(',')
        try:
            json.dump(inlist[len(inlist) - 1], outfile, ensure_ascii=False)
        except:
            pass
        outfile.write(']')
    outfile.close()
def mapreducewords(textin):
    topK=7
    newtext = textin
    tempresult = open("tempresult.txt", "w")
    while(len(newtext) > 300):
        text = newtext[0:299]
        newtext = newtext[300:len(newtext)]
        combtokens, tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
        if(combtokens != None):
            for item in combtokens:
                tempresult.write(item['word'] + '\t1\n')
    combtokens, tokens = APISet.LexicalAnalysis.getLexicalAnalysis(newtext)
    if(combtokens != None):
        try:
            for item in combtokens:
                tempresult.write(item['word'] + '\t1\n')
        except:
            pass  
    tempresult.close()
                
    Dic = {}
    for line in open("tempresult.txt"):
        line = line.strip()
        word = line.split('\t', 1)[0]                
        try:
            temp = int(1)
            Dic[word] = Dic.get(word, 0) + temp
        except:
            pass
                    
    FinalList = sorted(Dic.items(), key=itemgetter(1), reverse=True)
    sumfre = 0
    readylist = []
    for key, values in FinalList[0:topK]:
        sumfre = sumfre + values
    for key, values in FinalList[0:topK]:
        readylist.append(key)
        readylist.append(values / sumfre)           
    print(readylist)
    os.remove("tempresult.txt")
    return readylist

def getsohunews(currentDate):
    inlist = []
    t = []
    
    path = Util.getDataPath(currentDate+os.sep)+'sohu' + currentDate + '.json'

    try:
        with open(path) as f:
            json_str = f.read()
            data = json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path, 'w')
        data.close()
    except:
        os.remove(path)
        data = open(path, 'w')
        data.close() 
    
    resp = request.urlopen('https://www.sohu.com/')
    html_data = resp.read().decode('utf-8')
    # print(html_data)
    # First box
    soup = bs(html_data, 'html.parser')
    temp = soup.find_all('div', attrs={'class':'news'})
    slist = temp[0].find_all('a')
    for item in slist:
        if len(item.attrs['title']) < 8:
            break
        if t.count(item.attrs['title']) == 0:
            # print('new news')
            
            print(item.attrs['title'])
            title = item.attrs['title']
           
            tempUrl=item.attrs['href']
            content=getContentWithRetry(tempUrl)
            if(content==None):
                print("cannot get content of news: "+title)
                continue
            else:
                print(content)
                pass
            t.append(title)
            newtext = content

            tempdiction = {}
            tempdiction['title'] = title
            tempdiction['jump'] = item.attrs['href']
            tempdiction['content'] = content
            
            if(len(newtext) > 300):
                tempdiction['keywords'] = mapreducewords(newtext)
            else:
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)
                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)
                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist
                print(readylist)
           
            inlist.append(tempdiction)
        else:print('already exist')
    # Second box
    temp = soup.find_all('div', attrs={'class':'list-mod list-mod-1'})
    slist = temp[0].find_all('a')
    for item in slist:
        if t.count(item.attrs['title']) == 0:
            title = item.attrs['title']
            t.append(title)
            print('new news')
            content = title
            print(title)
            tempUrl=item.attrs['href']
            if(tempUrl.find("http:")==-1):
                tempUrl='http:'+tempUrl
            content=getContentWithRetry(tempUrl)
                
            # for title only news, keyword will not be analzed at present
            if(content==None):
                print("cannot get content of news: "+title)
                continue
            else:
#                 print(content)
                pass
            #if content get, add the title to title list
            t.append(title)
            
            newtext = content

            tempdiction = {}
            tempdiction['title'] = title
            tempdiction['jump'] = item.attrs['href']
            tempdiction['content'] = content
            
            if(len(newtext) > 300):
                tempdiction['keywords'] = mapreducewords(newtext)                
            else:               
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)
                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)

                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist
                print(readylist)
            inlist.append(tempdiction)
        else:
            print('already exist')
    writeresult(path, inlist)

def getsinanews(currentDate):
    inlist = []
    t = []
    path = Util.getDataPath(currentDate+os.sep)+'sina' + currentDate + '.json'
    
    try:
        with open(path) as f:
            json_str = f.read()
            data = json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path, 'w')
        data.close()
    except:
        os.remove(path)
        data = open(path, 'w')
        data.close() 
    
    resp = request.urlopen('https://www.sina.com.cn/')
    html_data = resp.read().decode('utf-8')
    # First box
    soup = bs(html_data, 'html.parser')
    temp = soup.find_all('div', id='newslist_a')
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        print(item.string)
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            # print('new news')
            print(item.string)
            title = item.string
            
            tempUrl=item.attrs['href']
            content=getContentWithRetry(tempUrl)
            # for title only news, keyword will not be analzed at present
            if(content==None):
                print("cannot get content of news: "+title)
                continue
            else:
#                 print(content)
                pass
            #if content get, add the title to title list
            t.append(title)
            
            newtext = content

            tempdiction = {}
            tempdiction['title'] = title
            tempdiction['jump'] = item.attrs['href']
            tempdiction['content'] = content
            
            if(len(newtext) > 300):
                tempdiction['keywords'] = mapreducewords(newtext)
                
            else:
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)
                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)

                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist

                print(readylist)
            inlist.append(tempdiction)
            
        else:print('already exist')
   
    writeresult(path, inlist)
    
def getnetnews(currentDate):
    inlist = []
    t = []
    path = Util.getDataPath(currentDate+os.sep)+'net' + currentDate + '.json'
    try:
        with open(path) as f:
            json_str = f.read()
            data = json.loads(json_str)
            for item in data:
                inlist.append(item)
                t.append(item['title'])
    except IOError:
        data = open(path, 'w')
        data.close()
    except:
        os.remove(path)
        data = open(path, 'w')
        data.close() 
    
    resp = request.urlopen('http://www.163.com/')
    html_data = resp.read().decode('gbk', 'ignore')

    soup = bs(html_data, 'html.parser')
    temp = soup.find_all('div', attrs={'class':'yaowen_news'})
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        # print(item.string)
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            # print('new news')
            print(item.string)
            title = item.string
            
            tempUrl=item.attrs['href']
            content=getContentWithRetry(tempUrl)
            # for title only news, keyword will not be analzed at present
            if(content==None):
                print("cannot get content of news: "+title)
                continue
            else:
#                 print(content)
                pass
            #if content get, add the title to title list
            t.append(title)
            
            newtext = content
            tempdiction = {}
            tempdiction['title'] = title
            tempdiction['jump'] = item.attrs['href']
            tempdiction['content'] = content
            
            if(len(newtext) > 300):
                tempdiction['keywords'] = mapreducewords(newtext)
            else:    
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)

                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)
                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist
                print(readylist)
            inlist.append(tempdiction)
            
        else:print('already exist')
    writeresult(path, inlist)

def getfenghuangnews(currentDate):
    inlist = []
    t = []
    path = Util.getDataPath(currentDate+os.sep)+'fenghuang' + currentDate + '.json'
    
    try:
        with open(path) as f:
            json_str = f.read()
            data = json.loads(json_str)
            for item in data:
                t.append(item['title'])
                inlist.append(item)
    except IOError:
        data = open(path, 'w')
        data.close()
    except:
        os.remove(path)
        data = open(path, 'w')
        data.close()   
        
    try:
        resp = request.urlopen('http://www.ifeng.com/')
        html_data = resp.read().decode('utf-8', 'ignore')
    except http.client.IncompleteRead as e:
        html_data = e.partial.decode('utf-8')
    print('successful')

    soup = bs(html_data, 'html.parser')
    temp = soup.find_all('div', id='headLineDefault')
    slist = temp[0].find_all('a')
    print(len(slist))
    for item in slist:
        # print(item.string)
        if (item.string == None):
            continue
        if (not((item.attrs['href'][0:10] == 'http://new') | (item.attrs['href'][0:10] == 'https://ne'))):
            continue
        else:
            print(item.attrs['href'])
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            title = item.string
            tempUrl=item.attrs['href']
            content=getContentWithRetry(tempUrl)
            # for title only news, keyword will not be analzed at present
            if(content==None):
                print("cannot get content of news: "+title)
                continue
            else:
#                 print(content)
                pass
            #if content get, add the title to title list
            t.append(title)
            newtext = content

            tempdiction = {}
            tempdiction['title'] = item.string
            tempdiction['jump'] = item.attrs['href']
            tempdiction['content'] = content
            
            if(len(newtext) > 300):
                tempdiction['keywords'] = mapreducewords(newtext)
                
            else:
                
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)
                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)

                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist

                print(readylist)
            inlist.append(tempdiction)            
        else:
            print('already exist')
    writeresult(path, inlist)


def getxinhuanews(currentDate):
    inlist = []
    t = []
    path = Util.getDataPath(currentDate+os.sep)+'xinhua' + currentDate + '.json'
    try:
        with open(path) as f:
            json_str = f.read()
            data = json.loads(json_str)
            for item in data:
                t.append(item['title'])
                inlist.append(item)
    except IOError:
        data = open(path, 'w')
        data.close()
    except:
        os.remove(path)
        data = open(path, 'w')
        data.close()
    
    resp = request.urlopen('http://www.xinhuanet.com/')
    html_data = resp.read().decode('utf-8', 'ignore')
    soup = bs(html_data, 'html.parser')
    temp = soup.find_all('div', attrs={'class':'borderCont'})
    slist = temp[2].find_all('a')
    print(len(slist))
    
    for item in slist:
        # print(item.string)
        if (item.string == None):
            print('jump')
            continue
        if (len(item.string) > 8) & (t.count(item.string) == 0):
            print('OK')
            t.append(item.string)
            tempdiction = {}
            tempdiction['title'] = item.string
            tempdiction['jump'] = item.attrs['href']
               
            content = ''
            temp_data = request.urlopen(item.attrs['href'])
            temphtml = temp_data.read().decode('utf-8', 'ignore')
            tempsoup = bs(temphtml, 'html.parser')
            temptemp = tempsoup.find_all('div', id='p-detail')

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
            tempdiction['content'] = content
            newtext = content

            tempresult = open("tempresults.txt", "w")
            if(len(newtext) < 30):
                continue
            if(len(newtext) > 300):
                
                tempdiction['keywords'] = mapreducewords(newtext)
            else:
                readylist = []
                sumfre = 0
                print("NEW TEXT：" + newtext)
                title = newtext
                tempwords = []

                result = nlp.extract_keywords(newtext, top_k=default_top_k)

                for weight, word in result:
                    sumfre = sumfre + weight
                for weight, word in result:
                    readylist.append(word)
                    readylist.append(weight / sumfre)
                        
                tempdiction['keywords'] = readylist
                
                print(readylist)
            inlist.append(tempdiction)  
                
        
        else:print('already exist')
    writeresult(path, inlist)
def sleeptime(hour, minu, sec):
    return hour * 3600 + minu * 60 + sec

def test():
    readylist = []
    sumfre = 0
    newtext = "新华社北京4月2日电 4月2日，国家主席习近平向埃及总统塞西致贺电，祝贺塞西再次当选埃及总统。习近平在贺电中指出，中埃友谊源远流长、历久弥新。近年来，我同你保持密切交往，中埃政治互信不断深化，务实合作持续推进，人文交流更加活跃，两国人民的心贴得更紧，我对此感到欣慰。希望埃及人民在塞西总统领导下，在探索符合自身国情发展道路上继续取得更多重要成就。我高度重视中埃关系发展，愿同你一道继续努力，推动中埃全面战略伙伴关系不断迈上新台阶，更好造福两国和两国人民。"
    print(newtext)
    title = newtext
    tempwords = []

    result = nlp.extract_keywords(newtext, top_k=7)
    for weight, word in result:
        print(word + "\t" + str(weight))
    for weight, word in result:
        sumfre = sumfre + weight
    for weight, word in result:
        readylist.append(word)
        print(word + "\t" + str(weight / sumfre))
        readylist.append(weight / sumfre)    
    print(readylist)
# this is begining of main function
if __name__ == '__main__':
    nlp = BosonNLP('4T70m9OU.24533.fXkOVBLkOFVM')
    second = sleeptime(0, 60, 0)
    while(1 == 1):
        currentDate = Util.getDateInStr()
        isFolderExist=os.path.exists(Util.getDataPath(currentDate))
        if(isFolderExist==False):
            os.makedirs(Util.getDataPath(currentDate))
        try:
            getsohunews(currentDate)
            getsinanews(currentDate)
            getnetnews(currentDate)
            getxinhuanews(currentDate)
            getfenghuangnews(currentDate)
        except:
            pass
        time.sleep(second)






