import HowToClimb.matchFct as m
import HowToClimb.apicall as api
import HowToClimb.geometry as g 
import copy
# positions des deux junglers / leur team / TIMEFRAME / liste des positions par frame / isInCircle
# team 100 : start 0/0 : team 200 : start 14000/14000


# Not used anymore.
def getTheJunglersPositions(match, junglers):
    listPositions = m.extractPositions(match)
    listPositionJunglers = []
    for jungler in junglers:
        for id in listPositions.keys():
            if str(id) == str(jungler.get('id')):
                listPositionJunglers.append({'id':jungler.get('id'), 'team': jungler.get('team'), 'positions':listPositions.get(id)})
    return listPositionJunglers


# in : dic {positions:[]}
# out : dic {positions:[], invade:bool, botstart:bool}
def getJunglerStart(junglerPosition):
    junglerPositionOut = junglerPosition
    position = junglerPosition.get('positions')[2]
    RedSideNormalStart = g.isOnRedSide(15000, position.get('x'), position.get('y')) and junglerPosition.get('team')==200 
    BlueSideNormalStart = (not g.isOnRedSide(15000, position.get('x'), position.get('y'))) and junglerPosition.get('team')==100
    if RedSideNormalStart or BlueSideNormalStart:
        junglerPositionOut['invade'] = False
    else:
        junglerPositionOut['invade'] = True
    junglerPositionOut['botstart'] = g.isOnBotSide(position.get('x'), position.get('y'))
    return junglerPositionOut


# in : match, summonerName
# out : dic : {id:, name, team:, invade:, botstart:, positions:[]}
def getTheJungleRoot(match, junglerName):
    playerId = m.getPlayersIdByName(match, junglerName)
    jungler = m.extractPositionsByPlayerId(match, playerId)
    jungleRoot = {'name': junglerName, 'id':playerId, 'team': m.getPlayersTeamByParticipantId(match, playerId), 'positions':jungler.get(str(playerId))}
    jungleRoot = getJunglerStart(jungleRoot)
    return jungleRoot
                  
# in : list : dic : {id, team, botstart, invade, position}
# out : list : dic : {team, botstart, invade, list : dic : { timestamp, list [positions]}
def prepareCJDatas(jungleRootList, team, botstart, invade):
    preparedData = {'team':team, 'botstart':botstart, 'invade':invade, 'positions':{}}
    for j in jungleRootList:
        if team==j.get('team') and botstart==j.get('botstart') and invade==j.get('invade'):
            for p in j.get('positions'):
                time = str(p.get('t'))
                if time in preparedData.get('positions'):
                    preparedData['positions'][time].append([p.get('x'), p.get('y')])
                else:
                    preparedData['positions'][time]=[]
                    preparedData['positions'][time].append([p.get('x'), p.get('y')])
    return preparedData

def clusterCJDatas(preparedDatas, radius, ncluster):
    preparedDatasCopy = copy.deepcopy(preparedDatas)
    data = preparedDatasCopy.get('positions')
    for k,v in data.items():
        data[k]=g.clustering(v, radius, ncluster)
    return preparedDatasCopy



# in : list : match 
# out : list : jungleRoot 
def prepareJungleRootList(matchList, summonerName):
    jungleRootList=[]
    for match in matchList:
        jungleRootList.append(getTheJungleRoot(match, summonerName))
    return jungleRootList




        
        


