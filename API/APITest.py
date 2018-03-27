# -*- coding: utf-8 -*-
'''

@author: andyh
'''

import sys
import os
sys.path.append("..")
from API import APISet



if __name__ == '__main__':
#     optional 
#   KeyWord Test
#     channel = "CHnews_news_tech"

    try:
        os.remove("temp.txt")
        os.remove("tempresult.txt")
    except:
        pass
 
    title = "闽宁镇的故事"
    content = """
    李克强谈“国税和地税合并”"""
    '''
    data = APISet.TextKeywords.getKeyword(title, content)
    if(data != None):
        for item in data:
            print("keyword=", item['keyword'])
            print("score=", item['score'])
            print("type=", item['type'])
    else:
        print("No data return")
'''

# contentGrabTest
#     url = 'http://new.qq.com/cmsn/20180305/20180305005930'
#     data = APISet.ContentGrab.getContent(url)
#     if(data != None):
#         print("code=", data['code'])
#         print("title=", data['title'])
#         print("content=", data['content'])
#     else:
#         print("No data return")
        
        
#     ContentTranscode Test
#     url='http://gd.ifeng.com/a/20180305/6408870_0.shtml'
#     data = APISet.ContentTranscode.getContentTranscode(url)
#     print(data)

    temp = open("temp.txt","w")
    tempresult = open("tempresult.txt","w")
    text = """
    习近平的2018两会时间"""

    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
    if(combtokens != None):
        for item in combtokens:
#             print("cls=", item['cls'])
#             print("pos=", item['pos'])
#             print("wlen=", item['wlen'])
            print("word=", item['word'])

            tempresult.write(item['word']+'\t1\n')
    if(tokens!=None):
        for item in tokens:
#             print("pos=", item['pos'])
#             print("wlen=", item['wlen'])
                
            #print("word=", item['word'])
            #print("wtype=", item['wtype'])
            #print(item['wtype_pos'])
            
#             print("wtype_pos=",item["wtype_pos"])
            i = int(item['wtype_pos'])
                #print(i)
            if((i==16) | (i==17) | (i==20) | (i==21) | (i==21)):
                print(item['word'])
                print('.........................')
                temp.write(item['word']+'\t1\n')
    
    else:
        print("No data return")

    temp.close()
    tempresult.close()


    

