import copy
# Fonctions utiles

def isOnRedSide(squareSide,x,y):
    return x >= (squareSide - y)

def isOnBotSide(x, y):
    return x >= y

# Créé des groupes de points
# in listPoint : [[x,y],..]
def groupPoints(listPoint, radius):
    listCluster = []
    for pRef in listPoint:
        pointRef = {str(pRef):[]}
        for point in listPoint:
            d = (((pRef[0]-point[0])**2)+((pRef[1]-point[1])**2))**0.5
            if d <= radius:
                pointRef[str(pRef)].append(point)
        listCluster.append(pointRef)
    return listCluster

def deletePoints(listPoint1, listPoint2):
    for point in listPoint1:
        if point in listPoint2:
            listPoint2.remove(point)

def getLongestList(listDic):
    lenList = 0
    res = {}
    for dic in listDic:
        for k,v in dic.items():
            if len(v)>lenList:
                lenList = len(v)
                res = dic
    return res

def clustering(listPoint, radius, nclusters):
    listPointCopy = copy.deepcopy(listPoint)
    listCluster = []
    for c in range(nclusters):
        if len(listPointCopy)>0:
            listGroup = groupPoints(listPointCopy, radius)
            longestList = getLongestList(listGroup)
            listCluster.append(longestList)
            for k,v in longestList.items():
                deletePoints(v, listPointCopy)
    return listCluster





        