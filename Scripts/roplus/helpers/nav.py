import BigWorld
import helpers.navigator
import Math
import math
import formula
import types
from data import seeker_data as SeekerData
from guis import uiUtils

import roplus
from roplus.helpers import maths

import time

lastPathFindDestination = None


def stopMove():
    player = BigWorld.player()
    navInst = helpers.navigator.getNav()
    if player and navInst:
        navInst.stopPathFinding()


def moveToEntityPathFind(entity):
    p = BigWorld.player()
    moveToPathFind((entity.position.x, entity.position.y, entity.position.z, p.mapID))


def moveToPathFind(destination):
    global lastPathFindDestination
    player = BigWorld.player()
    navInst = helpers.navigator.getNav()
    destPos = Math.Vector3(destination[0], destination[1], destination[2])
    if player and navInst:
        if not player.isPathfinding or not lastPathFindDestination or lastPathFindDestination.distTo(destPos) > 3:
            lastPathFindDestination = destPos
            navInst.pathFinding(destination, None, None, False, 0.5)


def getDestinationBySeekId(seekId):
    p = BigWorld.player()
    if type(seekId) == str:
        seekId = eval(seekId)
    if type(seekId) == types.TupleType:
        idList = list(seekId)
        minDis = -1
        spaceDelta = -1
        index = 0
        for item in idList:
            data = SeekerData.data.get(item, None)
            if data:
                pos = Math.Vector3(data['xpos'], data['ypos'], data['zpos'])
                spaceNo = data['spaceNo']
                if p.mapID != spaceNo and p.mapID in data.get('sharedMaps', ()):
                    spaceNo = p.mapID
                tempDis = (p.position - pos).length
                tempSpaceDelta = math.fabs(p.mapID - formula.getMapId(spaceNo))
                if spaceDelta == -1 or spaceDelta > tempSpaceDelta or tempSpaceDelta == spaceDelta and (
                                minDis == -1 or minDis > tempDis):
                    spaceDelta = tempSpaceDelta
                    minDis = tempDis
                    index = item
        seekId = index
    if not p:
        return None
    if type(seekId) is not int:
        return None
    if not SeekerData.data.has_key(seekId):
        return None
    seekerData = SeekerData.data[seekId]
    pos = Math.Vector3(seekerData["xpos"], seekerData["ypos"], seekerData["zpos"])
    spaceNo = seekerData["spaceNo"]
    if p.mapID != spaceNo and p.mapID in seekerData.get("sharedMaps", ()):
        spaceNo = p.mapID
    ent = uiUtils.searchEnt(seekId, 80)
    if ent:
        pos = ent.position
    return pos.x, pos.y, pos.z, spaceNo
