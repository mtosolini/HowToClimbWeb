import apicall as ac
import myRateLimiter as mrl
# championIds : [id1,id2,...,idn]
# rankedQueues:  [TEAM_BUILDER_DRAFT_RANKED_5x5, RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5]
# seasons: [PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015, PRESEASON2016, SEASON2016]
# beginTime : long
# endTime   : long
# beginIndex: int
# endIndex  : int
'''
ac.getSummonerMatchListBySummonerName('euw', 'starCrafT243ver', mrl.RateLimiter())
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(), championIds=[112,113,114])
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(), rankedQueues='RANKED_SOLO_5x5')
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(), seasons=['PRESEASON2015', 'SEASON2015'])
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(),championIds= 112)
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(),championIds = [112,113,114],
rankedQueues=  ['TEAM_BUILDER_DRAFT_RANKED_5x5', 'RANKED_SOLO_5x5', 'RANKED_TEAM_3x3', 'RANKED_TEAM_5x5'],
 seasons= ['PRESEASON3', 'SEASON3', 'PRESEASON2014', 'SEASON2014', 'PRESEASON2015', 'SEASON2015', 'PRESEASON2016', 'SEASON2016'],
 beginTime= 15,
 endTime= "100",
 beginIndex=10,
 endIndex  = 1000)
ac.getSummonerMatchListBySummonerName('euw', 'starcraft243ver', mrl.RateLimiter(),championIds = [112,113,114],
rankedQueues=  ['TEAM_BUILDER_DRAFT_RANKED_5x5', 'RANKED_SOLO_5x5', 'RANKED_TEAM_3x3', 'RANKED_TEAM_5x5'],
 seasons= ['PRESEASON3', 'SEASON3', 'PRESEASON2014', 'SEASON2014', 'PRESEASON2015', 'SEASON2015', 'PRESEASON2016', 'SEASON2016'])
'''
# return the list of the full matches infos of the player, for the given region, filtered by **kwarg :
# championIds : [id1,id2,...,idn]
# lane:   [MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM]
# rankedQueues:  [TEAM_BUILDER_DRAFT_RANKED_5x5, RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5]
# role:   [DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT]
# seasons: [PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015, PRESEASON2016, SEASON2016]
# n : int (number of games)
# timeLine : str : true/false
#ac.getLastMatches('euw', 'starcraft243ver', mrl.RateLimiter(), timeLine='true', lane='MID', n=14, seasons=['SEASON2016','SEASON2014'])
#ac.getLastMatches('euw', 'starcraft243ver', mrl.RateLimiter(), lane=['MID', 'JUNGLE'], seasons=['SEASON2016','SEASON2014'])