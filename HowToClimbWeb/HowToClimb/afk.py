import HowToClimb.apicall as api
import HowToClimb.matchFct as matchFct
from collections import Counter

def countAfkInGame(_match, summonerName):
    listPositions = matchFct.extractPositions(_match)
    mainPlayerId = matchFct.getPlayersIdByName(_match, summonerName)
    mainPlayerTeam = matchFct.getPlayersTeamByParticipantId(_match, mainPlayerId)
    afkStats = {
        'GameInfos' : {'matchId' : _match.get('matchId'), 'afk' : False, 'win' : matchFct.hasWonSummonerId(_match, mainPlayerId)},
        'whoAfk' : {
            'opponent' : {'short': 0, 'medium': 0, 'long': 0}, 
            'allied' : {'short': 0, 'medium': 0, 'long': 0}, 
            'self' : {'short': 0, 'medium': 0, 'long': 0} 
            }}        
    for player, positions in listPositions.items():
        timeAfk = countTimeAfk(positions)
        if timeAfk >= 2:
            afkStats['GameInfos']['afk']= True
            if timeAfk >= 2 and timeAfk < 5:
                keyTime = 'short'
            if timeAfk >= 5 and timeAfk < 15:
                keyTime = 'medium'
            if timeAfk >=15:
                keyTime = 'long'
            if str(mainPlayerTeam) == str(matchFct.getPlayersTeamByParticipantId(_match, player)):
                if str(player)==str(mainPlayerId):
                    afkStats['whoAfk']['self'][keyTime]+=1
                else:
                    afkStats['whoAfk']['allied'][keyTime]+=1
            else:
                afkStats['whoAfk']['opponent'][keyTime]+=1
    return afkStats

def sumTheAfk(totalAfk, newAfk):
     return {k: totalAfk.get(k, 0) + newAfk.get(k, 0) for k in set(totalAfk) | set(newAfk)}
        
def countTimeAfk(positions):
    x = -1
    y = -1
    timeAfk = 0
    for position in positions:
        if position != None:
            if position.get('x')== x and position.get('y')==y:
                timeAfk+=1
            x = position.get('x')
            y = position.get('y')
    return timeAfk

def GetAllAfk(summoner, n, _apiCst, _region):
    listMatches = api.getLastMatches(_region, summoner, _apiCst, m=n, timeLine='true', seasons='SEASON2016')
    totalAfk = { 
        'self' : { 'short' : 0, 'medium' : 0, 'long' : 0 },
        'opponent': { 'short' : 0, 'medium' : 0, 'long' : 0 },
        'allied': { 'short' : 0, 'medium' : 0, 'long' : 0 }}
    #print('Matchs trouvés : '+str(len(listMatches)))
    detail = []
    for match in listMatches:
        afkResult = countAfkInGame(match, summoner)
        if afkResult.get('GameInfos').get('afk'):
            #print(afkResult) 
            detail.append(afkResult)
            totalAfk['opponent'] = sumTheAfk(totalAfk.get('opponent'), afkResult.get('whoAfk').get('opponent'))
            totalAfk['allied'] = sumTheAfk(totalAfk.get('allied'), afkResult.get('whoAfk').get('allied'))
            totalAfk['self'] = sumTheAfk(totalAfk.get('self'), afkResult.get('whoAfk').get('self'))
    #print('Total des Afk :')
    #print(totalAfk)
    afk = {'totalAfk' : totalAfk, 'totalGames' : len(listMatches), 'detailGames':detail}
    return afk


