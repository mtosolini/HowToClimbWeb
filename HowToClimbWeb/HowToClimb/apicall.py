import requests
import time

#API functions and stuff

# get the profile by summoner name
def getSummonerProfileByName(_region, _summonerNames, _apiCst):
    url = _apiCst.instance.apiUrl[_region]+"/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}?api_key={key}"
    url = url.format(region = _region , summonerNames = _summonerNames, key = _apiCst.instance.key)
    request = requestWrapper(_region, url, _apiCst)
    return request.json()


# return the list of the full matches infos of the player, for the given region, filtered by **kwarg :
# championIds : [id1,id2,...,idn]
# lane:   [MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM]
# rankedQueues:  [TEAM_BUILDER_DRAFT_RANKED_5x5, RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5]
# role:   [DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT]
# seasons: [PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015, PRESEASON2016, SEASON2016]
# n : int (look the last n games only)
# m : int (return m games or all if m > totalGames)
# timeLine : str : true/false

def getLastMatches(region, name, rateLimiter, **kwarg):
    # Get the summarized list of the matches
    listMatchId = getSummonerMatchListBySummonerName(region, name, rateLimiter,**kwarg).get('matches', [])
    listMatch = []
    listMatchNotFound = []
    for match in listMatchId[:kwarg.get('n',len(listMatchId))]:
        # Filter by lane/role
        if (match.get('lane', '') in kwarg.get('lane', ['MID', 'MIDDLE', 'TOP', 'JUNGLE', 'BOT', 'BOTTOM',''])
                                           and match.get('role', '') 
                                           in kwarg.get('role',['DUO', 'NONE', 'SOLO', 'DUO_CARRY', 'DUO_SUPPORT',''])):
            # Build the request
            url = rateLimiter.instance.apiUrl[region]+'/api/lol/{region}/v2.2/match/{matchId}?includeTimeline={timeLine}&api_key={key}'
            url = url.format(region=region, matchId = match.get('matchId'), timeLine = kwarg.get('timeLine','false')
                             , key = rateLimiter.instance.key)
            # Process
            request = requestWrapper(region, url, rateLimiter)
            if request==None:
                # Get the matches which couldnt be found (later use)
                listMatchNotFound.append(match.get('matchId'))
                print('Game: '+str(match.get('matchId'))+' echouée')
            else:
                # We get the match
                listMatch.append(request.json())
                print('Game: '+str(match.get('matchId'))+' chargée')
        # cut the loop if we have the number of games asked
        if len(listMatch)==kwarg.get('m', -1):
            return listMatch                  
    return listMatch

# return the short list of the player's match for the given region, filtered by **kwarg :
# championIds : [id1,id2,...,idn]
# rankedQueues:  [TEAM_BUILDER_DRAFT_RANKED_5x5, RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5]
# seasons: [PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015, PRESEASON2016, SEASON2016]
# beginTime : long
# endTime   : long
# beginIndex: int
# endIndex  : int

def getSummonerMatchListBySummonerName(region, name, rateLimiter, **kwarg):
    # Build the request base
    url = rateLimiter.instance.apiUrl[region]+"/api/lol/{region}/v2.2/matchlist/by-summoner/{summonerId}?{param}api_key={key}"
    param = ""
    authorizedParams = ['championIds','rankedQueues','seasons','beginTime','endTime','beginIndex','endIndex']
    # Build the requests parameters
    for key, value in kwarg.items():
        if key in authorizedParams:
            param = param+str(key)+"="+str(value).replace('[','').replace(']','').replace(' ','').replace("'", '').replace('"','')+"&"
    summonerId = getSummonerProfileByName(region, name, rateLimiter)[name.lower()]['id']
    url = url.format(region=region, summonerId=summonerId,param=param, key=rateLimiter.instance.key)
    # Process
    request = requestWrapper(region, url, rateLimiter)
    if request != None:
        return request.json()
    return {'err':-1} 


# Wrapper for requests
def requestWrapper(_region, _url, _apiCst):
    _apiCst.rateLimitWaiter(_region)
    request = requests.get(_url)
    retryCounter = 0
    while request.status_code!=200 and request.headers.get('X-Rate-Limit-Type')==None and retryCounter < 5:
        print('Fail : retry : '+str(retryCounter))
        retryCounter+=1
        _apiCst.rateLimitWaiter(_region)
        request = requests.get(_url)
    if request.headers.get('X-Rate-Limit-Type')=='service':
        if request.headers.get('Retry-After')!=None:
            print('Service saturé pour: '+str(request.headers.get('Retry-After'))+'s')
            time.sleep(request.headers.get('Retry-After'))
            _apiCst.rateLimitWaiter(_region)
            request = requests.get(_url)
    elif request.headers.get('X-Rate-Limit-Type')=='user':
        print('Refais ta fonction de rateLimitWaiter ...')
    # Si ça ne marche toujours pas ...
    if request.status_code!=200:
        print('Problème avec la game :'+_url)
        print('Status_code: '+str(request.status_code))
        print('X-Rate-Limit-Type:'+str(request.headers.get('X-Rate-Limit-Type')))
        print('Retry-After: '+str(request.headers.get('Retry-After')))
        print('X-Rate-Limit-Count: '+request.headers.get('X-Rate-Limit-Count'))
        return None
    else:
        print('Api call Success :'+_url)
    return request
        

###################################################
###################################################

# get the list of the matches of the player
# wtf i dont know if someone if going to use this
'''def getSummonerMatchListById(_region, _summonerId, _apiCst):
    url = _apiCst.instance.apiUrl[_region]+"/api/lol/{region}/v2.2/matchlist/by-summoner/{summonerId}?api_key={key}"
    url = url.format(region =_region, summonerId = _summonerId, key = _apiCst.instance.key)
    request = requestWrapper(_region, url, _apiCst)
    return request.json()

def getSummonerMatchListBySummonerNameOld(_region, _summonerNames, _apiCst):
    url = _apiCst.instance.apiUrl[_region]+"/api/lol/{region}/v2.2/matchlist/by-summoner/{summonerId}?api_key={key}"
    _summonerId = getSummonerProfileByName(_region, _summonerNames, _apiCst)[_summonerNames.lower()]['id']
    url = url.format(region = _region, summonerId = _summonerId, key = _apiCst.instance.key)
    _request = requestWrapper(_region, url, _apiCst)
    return _request.json()'''



# not used anymore : see getLastMatches
'''def getLastMatchesOld(_region, _summonerNames, _numberOfMatches, _apiCst, _Timeline, _queueType, _lane, _season):
    _apiCst.rateLimitWaiter(_region)
    listMatchId = getSummonerMatchListBySummonerName(_region, _summonerNames, _apiCst).get('matches', [])
    listMatch = []
    i=0
    for match in listMatchId[:_numberOfMatches]:
        if match.get('queue') in _queueType and match.get('season') in _season and match.get('lane') in _lane:
            url = _apiCst.instance.apiUrl[_region]+'/api/lol/{region}/v2.2/match/{matchId}?includeTimeline=true&api_key={key}'
            url = url.format(region = _region, matchId = match.get('matchId'), Timeline = _Timeline, key = _apiCst.instance.key)
            request = requestWrapper(_region,url, _apiCst)
            if request!=None:
                print('Game: '+str(match.get('matchId'))+' chargée')
                listMatch.append(request.json())
            else:
                print('Game: '+str(match.get('matchId'))+' echouée')   
    return listMatch'''