# -*- coding: utf-8 -*-
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
        if(result == None):
            return
        data = json.loads(result.decode('utf-8'))
        if(result != None and data["code"] != 0):
            return None
        else:
            return data['keywords']
class ContentGrab(object):
    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def getContent(url):
        '''
    parameter:
        url:The target url
    return:
        data:The result in json format.Fields contained:keyword,score,type
        use data['keyword'] to access
    '''
        module = 'wenzhi'
        action = 'ContentGrab'
        region = "sz"
        path = DataLoader.getDataPath("keys/keys2.txt")
        with open(path) as f:
            secretId = f.readline().strip('\n')
            secretKey = f.readline().strip('\n')
        config = {
            'Region': region,
            'secretId': secretId,
            'secretKey': secretKey}
        action_params = {
            'url':url
        }
        try:
            service = QcloudApi(module, config)
            #print(service.generateUrl(action, action_params))
            result = service.call(action, action_params)
            print(result)
        except Exception as e:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
        if(result == None):
            return
        data = json.loads(result.decode('utf-8'))
        if(result != None and data["code"] != 0):
            return None
        else:
            return data
class LexicalAnalysis(object):
    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def getLexicalAnalysis(text, code=0x00200000, searchType=0):
        '''
    parameter:
        text:The text that need to be split
        code:The coding scheme 
        searchType:The search type 
        取值0或1，默认为0。 0为基础粒度版分词，倾向于将句子切分的更细，在搜索场景使用为佳。 1为混合粒度版分词，倾向于保留更多基本短语不被切分开。
    return:
        combtokens:The phrase obtained 
        tokens:The token obtained
    '''
        module = 'wenzhi'
        action = 'LexicalAnalysis'
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
            "text":text,
            "code":code,
            "type":searchType
        }
        try:
            service = QcloudApi(module, config)
            print(service.generateUrl(action, action_params))
            result = service.call(action, action_params)
            print(result)
        except Exception as e:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
        if(result == None):
            return None, None
        data = json.loads(result.decode('utf-8'))
        if(result != None and data["code"] != 0):
            return None, None
        else:
            return data["combtokens"], data["tokens"]
class ContentTranscode(object):
    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def getContentTranscode(url):
        '''
    parameter:
        url:The target url
    return:
        data
    '''
        module = 'wenzhi'
        action = 'ContentTranscode'
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
            'url':url
        }
        try:
            service = QcloudApi(module, config)
            print(service.generateUrl(action, action_params))
            result = service.call(action, action_params)
            print(result)
        except Exception as e:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
        if(result == None):
            return
        data = json.loads(result.decode('utf-8'))
        if(result != None and data["code"] != 0):
            return None
        else:
            return data
