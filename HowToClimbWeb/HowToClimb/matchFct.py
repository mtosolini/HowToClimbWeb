import HowToClimb.var as var
import HowToClimb.apicall as api

def getIdByRole(match, _lane):
    lane = []
    for participant in match.get('participants'):
        if participant.get('timeline').get('lane') in _lane:
            lane.append({'id': participant.get('participantId'), 'team': participant.get('teamId')})
    if len(lane)!=0 :
        return lane
    print('Role not found')
    return -1


def getPlayersTeamByParticipantId(_match, _participantId):
    for participant in _match.get('participants'):
        if str(_participantId) == str(participant.get('participantId')):
            return participant.get('teamId')
    print('TeamNotFound')
    return -1

def getPlayersNameByParticipantId(_match, _participantId):
    for participantIdentity in _match.get('participantIdentities'):
        if str(_participantId) == str(participantIdentity.get('participantId')):
            return participantIdentity.get('player').get('summonerName')
    print('Joueur introuvable')
    return 'playerNotFound'

def getPlayersIdByName(match, playerName):
    for participantIdentity in match.get('participantIdentities'):
        if participantIdentity.get('player').get('summonerName').lower()==playerName.lower():
            return participantIdentity.get('participantId')
    print('Joueur pas dans la partie')
    return -1

def hasWonSummonerId(match, playerId):
    try:
        TeamPlayerId = getPlayersTeamByParticipantId(match, playerId)
        for team in match.get('teams'):
            if str(team.get('teamId'))==str(TeamPlayerId):
                return team.get('winner')
    except:
        print('Winner introuvable')

def hasWonSummonerName(match, summonerName):
    try:
        playerId = getPlayersIdByName(match, summonerName)
        TeamPlayerId = getPlayersTeamByParticipantId(match, playerId)
        for team in match.get('teams'):
            if str(team.get('teamId'))==str(TeamPlayerId):
                return team.get('winner')
    except:
        print('Winner introuvable')

# Extract all the positions of the players with the timestamp associated
def extractPositions(_match, timeAccuracy = 1):
    listPositions = { }
    if 'timeline' in _match:
       for frames in _match.get('timeline').get('frames'):
            players = frames.get('participantFrames')
            for player in players.items():
                if 'participantId' in player[1]:
                    playerId = str(player[1].get('participantId'))
                    if playerId in listPositions:
                        position = player[1].get('position')
                        if 'position' in player[1]:
                            position['t'] = int(frames.get('timestamp')/(1000/timeAccuracy))
                            listPositions.get(playerId).append(position)
                    else:
                        position = player[1].get('position')
                        if 'position' in player[1]:
                            position['t'] = int(frames.get('timestamp')/(1000/timeAccuracy))
                            listPositions[playerId]=[]
                            listPositions.get(playerId).append(position)
    return listPositions
    
#Extract all the positions of one of the player, based on the Id
def extractPositionsByPlayerId(_match, _playerId, timeAccuracy = 1):
    listPositions = {str(_playerId) : []}
    if 'timeline' in _match:
       for frames in _match.get('timeline').get('frames'):
            players = frames.get('participantFrames')
            for player in players.items():
                if 'participantId' in player[1]:
                    if int(player[1].get('participantId'))==int(_playerId):
                        if 'position' in player[1]:
                            position = player[1].get('position')
                            position['t'] = int(frames.get('timestamp')/(1000/timeAccuracy))
                            listPositions.get(str(_playerId)).append(position)
    return listPositions


def returnedToFountain(event, team, idPlayer):
	if event.get('eventType')=='ITEM_PURCHASED' and str(event.get('participantId'))==str(idPlayer) :
		if team == 100:
			return {'t':event.get('timestamp'), 
			'x': 500, 
			'y': 500}
		if team == 200:
			return {'t':event.get('timestamp'), 
			'x': 14500, 
			'y': 14500}
	return -1

def championKilled(event, idPlayer):
	if event.get('eventType')=='CHAMPION_KILL':
		if str(event.get('killerId'))==str(idPlayer) or int(idPlayer) in event.get('assistingParticipantIds'):
			return {'x':event.get('position').get('x'),
			'y':event.get('position').get('y'),
			't':event.get('timestamp')}
	return -1
	
def eliteMonsterKilled(event, idPlayer):
	if event.get('eventType')=='ELITE_MONSTER_KILL':
		if str(event.get('killerId'))==str(idPlayer):
			return {'x':event.get('position').get('x'),
			'y':event.get('position').get('y'),
			't':event.get('timestamp')}
	return -1	
	
def buildingKill(event, idPlayer):
	if event.get('eventType')=='BUILDING_KILL':
		if str(event.get('killerId'))==str(idPlayer) or int(idPlayer) in event.get('assistingParticipantIds'):
			return {'x':event.get('position').get('x'),
			'y':event.get('position').get('y'),
			't':event.get('timestamp')}
	return -1
