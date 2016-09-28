#################################################
# TODO : Faire un truc avec des threads et tout
#################################################

import time 

class RateLimiter:
    class __RateLimiter:
        def __init__(self):
            with open('HowToClimb/ApiKey.txt') as constant:
                self.key = constant.read()
            self.calls = {'euw': 0}
            self.firstCall = {'euw' : time.time()}
            self.lastCall = {'euw' : time.time()}
            self.rate = {'euw' : 1.21}
            self.apiUrl = {'euw' : 'https://euw.api.pvp.net' }

        def __str__(self):
            return repr(self) + self.apiUrl.get('euw')
    instance = None

    def __init__(self):
        if not RateLimiter.instance:
            RateLimiter.instance = RateLimiter.__RateLimiter()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def rateLimitWaiter(self, region):
        timestamp = time.time() - RateLimiter.instance.lastCall[region]
        if timestamp < RateLimiter.instance.rate[region]:
            time.sleep(RateLimiter.instance.rate[region]-timestamp)
        RateLimiter.instance.lastCall[region]=time.time()
        RateLimiter.instance.calls[region]+=1
        #print(self.instance.calls[region])
    