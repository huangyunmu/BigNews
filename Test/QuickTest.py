'''

@author: andyh
'''
# for code quick testing
import random
import time
from API import APISet
if __name__ == '__main__':
    worker=APISet.ContentGrab
    retryCount=0
    retryLimit=5
    url="http://www.sohu.com/a/226924934_362042?g=0?code=9bbfcdc2cd795e8e8711313c96365c78"
    retryIntervalBegin=2
    retryInterval=retryIntervalBegin
    retryInterValLimit=32
    while(retryCount<retryLimit):
        data=worker.getContent(url)
        if(data!=None):
            print(data["content"])
            retryInterval=retryIntervalBegin
            break
        time.sleep(retryInterval)
        if(retryInterval<retryInterValLimit):
            retryInterval=retryInterval*2
        retryCount=retryCount+1
        print("retryCount:"+str(retryCount))
        print("retryInterval:"+str(retryInterval))
#     print(random.randint(5,10))
    