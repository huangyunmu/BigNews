# -*- coding: utf-8 -*-
'''

@author: andyh
'''
import sys
from API import APISet


sys.path.append("..")
if __name__ == '__main__':
#     optional 
#   KeyWord Test
#     channel = "CHnews_news_tech"
    title = "闽宁镇的故事"
    content = """
    闽宁镇，这个当年由习近平亲自命名的扶贫移民区，已从一个“天上无飞雀，地上不长草，风吹沙石跑”的荒芜之地，发展成为常住居民6万余人的特色小镇。
　　1997年，福建和宁夏启动了对口扶贫协作。作为起点，闽宁镇从无到有、由弱到强，见证了闽、宁携手从单向扶贫到互利共赢的20载
　　2016年7月19日，习总书记到闽宁镇视察时曾给予高度肯定并指出：“闽宁镇从当年的‘干沙滩’变成了今天的‘金沙滩’，探索出了一条康庄大道，我们要把这个宝贵经验向全国推广。”
　　如今，曾经的戈壁荒滩变成了现代化的生态移民示范镇，6万多名曾经生活在贫困山区的农民走出大山搬入闽宁镇，通过移民搬迁走上了脱贫致富之路。
    """
    data = APISet.TextKeywords.getKeyword(title, content)
    if(data != None):
        for item in data:
            print("keyword=", item['keyword'])
            print("score=", item['score'])
            print("type=", item['type'])
    else:
        print("No data return")

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

    text = """
    闽宁镇，这个当年由习近平亲自命名的扶贫移民区，已从一个“天上无飞雀，地上不长草，风吹沙石跑”的荒芜之地，发展成为常住居民6万余人的特色小镇。
　　1997年，福建和宁夏启动了对口扶贫协作。作为起点，闽宁镇从无到有、由弱到强，见证了闽、宁携手从单向扶贫到互利共赢的20载
　　2016年7月19日，习总书记到闽宁镇视察时曾给予高度肯定并指出：“闽宁镇从当年的‘干沙滩’变成了今天的‘金沙滩’，探索出了一条康庄大道，我们要把这个宝贵经验向全国推广。”
　　如今，曾经的戈壁荒滩变成了现代化的生态移民示范镇，6万多名曾经生活在贫困山区的农民走出大山搬入闽宁镇，通过移民搬迁走上了脱贫致富之路。
    """
    combtokens,tokens = APISet.LexicalAnalysis.getLexicalAnalysis(text)
    if(combtokens != None):
        for item in combtokens:
#             print("cls=", item['cls'])
#             print("pos=", item['pos'])
#             print("wlen=", item['wlen'])
            print("word=", item['word'])
    if(tokens!=None):
        for item in tokens:
#             print("pos=", item['pos'])
#             print("wlen=", item['wlen'])
            print("word=", item['word'])
            print("wtype=", item['wtype'])
#             print("wtype_pos=",item["wtype_pos"])
    
    else:
        print("No data return")
    
    
    
