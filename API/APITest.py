# -*- coding: utf-8 -*-
'''

@author: andyh
'''
from API import APISet
from Util import DataLoader
if __name__ == '__main__':
#     optional 
#     channel = "CHnews_news_tech"
    title="Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330"
    content="Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330"
    data=APISet.TextKeywords.getKeyword(title, content)
    if(data!=None):
        for item in data:
            print("keyword=",item['keyword'])
            print("score=",item['score'])
            print("type=",item['type'])
    else:
        print("No data return")
#     path=DataLoader.getDataPath("keys/keys.txt")
#     with open(path) as f:
#         secreId=f.read()
#         key=f.read()
#     print(secreId,key)
    
    
    
