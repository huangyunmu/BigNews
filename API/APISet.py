'''

@author: andyh
'''
import sys
sys.path.append("..")
import traceback
import json
from QcloudApi.qcloudapi import QcloudApi
from Util import DataLoader
class TextKeywords(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def getKeyword(title, content, channel="CHnews_news_tech"):
        '''
    parameter:
        title:The title of news
        content:The content of news
        channel:The channel that the news belongs to.(Optional, the default value is tech)
    return:
        data:The result in json format.Fields contained:keyword,score,type
        use data['keyword'] to access
    '''
        module = 'wenzhi'
        action = 'TextKeywords'
        region = "sz"
        path = DataLoader.getDataPath("keys/keys.txt")
        with open(path) as f:
            secretId = f.readline().strip('\n')
            secretKey = f.readline().strip('\n')
        config = {
            'Region': region,
            'secretId': secretId,
            'secretKey': secretKey}
        action_params = {
            'title': title,
            'content':content
        }
        try:
            service = QcloudApi(module, config)
            print(service.generateUrl(action, action_params))
            result = service.call(action, action_params)
            print(result)
        except Exception as e:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
        if(result==None):
            return
        data = json.loads(result.decode('utf-8'))
        if(result!=None and data["code"] != 0):
            return None
        else:
            return data['keywords']
