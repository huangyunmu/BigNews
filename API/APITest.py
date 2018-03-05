# -*- coding: utf-8 -*-
'''

@author: andyh
'''
import sys
import json
from API import APISet
from Util import DataLoader


sys.path.append("..")
if __name__ == '__main__':
#     optional 
#   KeyWord Test
#     channel = "CHnews_news_tech"
#     title = "Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330"
#     content = "Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330"
#     data = APISet.TextKeywords.getKeyword(title, content)
#     if(data != None):
#         for item in data:
#             print("keyword=", item['keyword'])
#             print("score=", item['score'])
#             print("type=", item['type'])
#     else:
#         print("No data return")

# contentGrabTest
    url = 'http://new.qq.com/cmsn/20180305/20180305005930'
    data = APISet.ContentGrab.getContent(url)
    if(data != None):
        print("code=",data['code'])
        print("title=",data['title'])
        print("content=",data['content'])
    else:
        print("No data return")
    
#     url='http://gd.ifeng.com/a/20180305/6408870_0.shtml'
#     data = APISet.ContentTranscode.getContentTranscode(url)
#     print(data)
    
    
    
