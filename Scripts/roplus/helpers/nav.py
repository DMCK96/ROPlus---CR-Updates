import BigWorld
import helpers.navigator

from roplus.helpers import maths

import time

lastPathFindRequestTimestamp = 0

def stopMove():
    player = BigWorld.player()
    navInst = helpers.navigator.getNav()
    if player and navInst:
        navInst.stopPathFinding()
        

def moveToPathFind(destination):
    global lastPathFindRequestTimestamp
    player = BigWorld.player()
    navInst = helpers.navigator.getNav()
    if player and navInst:
        if time.time() - lastPathFindRequestTimestamp > 2 and (not navInst.currentDst or maths.getDistance3D(destination, navInst.currentDst) > 1):
            lastPathFindRequestTimestamp = time.time()
            navInst.pathFinding(destination, None, None, False, 0.5)