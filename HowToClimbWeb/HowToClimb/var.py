
#***************************************
# NOT USED ANYMORE SEE myRateLimiter.py
#***************************************

import time
import os

class ApiCst():
    def __init__(self, region="euw", apiUrl="https://euw.api.pvp.net"):
        with open('HowToClimb/ApiKey.txt') as constant:
            self.key = constant.read()
        self.region = region
        self.calls = 0
        self.firstCall = time.time()
        self.lastCall = time.time()
        self.rate = 1.21
        self.apiUrl = apiUrl

    def rateLimitWaiter(self):
        timestamp = time.time() - self.lastCall
        if timestamp < self.rate:
            time.sleep(self.rate - timestamp)
            self.lastCall = time.time()
            self.calls+=1

    def catchRateLimit(self, rqst):
        ''' Debug purpose only '''
        if rqst.status_code!=200:
            print("Code d'erreur: "+str(rqst.status_code))
            if rqst.status_code==429:
                print(rqst.headers.get('X-Rate-Limit-Type'))
                print(rqst.headers.get('Retry-After'))
                print(rqst.headers.get('X-Rate-Limit-Count'))

