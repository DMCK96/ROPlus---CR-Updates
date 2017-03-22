import math

import BigWorld

def getDistance3D(pos1, pos2):
    return math.sqrt(math.pow((pos1[0]-pos2[0]),2) + math.pow((pos1[1]-pos2[1]),2) + math.pow((pos1[2]-pos2[2]),2))

def getDistance3DFromPlayer(pos):
    player = BigWorld.player()
    if player:
        return getDistance3D(pos, player.position)
    else:
        return 100000