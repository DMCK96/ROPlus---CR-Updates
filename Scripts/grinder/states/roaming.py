import roplus

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import nav

import BigWorld

class Roaming(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Roaming"
        self.currentHotspotIndex = 0
        self.lastPathFindTime = 0

    def needToRun(self):
        player = BigWorld.player()

        return player != None and player.hp > 0

    def run(self):
        hotspot = self.bot.currentProfile["hotspots"][self.currentHotspotIndex]
        if maths.getDistance3DFromPlayer(hotspot) >= 2:
            nav.moveToPathFind(hotspot)
        else:
            roplus.log("Moving to next hotspot ...")
            self.currentHotspotIndex += 1
            if self.currentHotspotIndex >= len(self.bot.currentProfile["hotspots"]):
                self.currentHotspotIndex = 0

    def onEnter(self):
        return None

    def onLeave(self):
        return None
