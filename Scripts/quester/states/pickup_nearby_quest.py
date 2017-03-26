import roplus

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import nav
from roplus.helpers import questing

from guis import uiUtils
import BigWorld

import time

class PickupNearbyQuest(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "PickupNearbyQuest"
        self.lastTaskRunTime = 0

    def needToRun(self):
        p = BigWorld.player()

        if not p:
            return False

        if p.isDoingAction:
            return False

        self.currentQuest = self.chooseQuest()

        return self.currentQuest and p != None and p.hp > 0

    def run(self):
        p = BigWorld.player()

        acNpc = None
        if "acNpc" in self.currentQuest.questData:
            for entity in p.entitiesInRange(100):
                if getattr(entity, "npcId", 0) == self.currentQuest.questData["acNpc"]:
                    acNpc = entity
                
        if acNpc:
            if p.position.distTo(acNpc.position) > 2:
                self.name = "Moving to pickup quest : " + self.currentQuest.getName()
                nav.moveToPathFind((acNpc.position.x, acNpc.position.y, acNpc.position.z, p.mapID))
                return
            else:
                self.name = "Pickup quest : " + self.currentQuest.getName()
                nav.stopMove()
                acNpc.acceptQuest(self.currentQuest.questId)
                self.bot.engine.wait(1)
                return

        if time.time() - self.lastTaskRunTime > 1:
            if "acNpcTk" in self.currentQuest.questData:
                uiUtils.findPosById(self.currentQuest.questData["acNpcTk"])
                self.lastTaskRunTime = time.time()
                self.name = "Moving to pickup quest : " + self.currentQuest.getName()
                return

    def onEnter(self):
        return None

    def onLeave(self):
        return None

    def chooseQuest(self):
        p = BigWorld.player()
        if not p:
            return None

        quests = questing.getQuestInfosFromCache("available_tasks")
        if quests and len(quests) > 0:
            for entity in p.entitiesInRange(1000):
                if getattr(entity, "npcId", 0) != 0:
                    for quest in quests:
                        if "acNpc" in quest.questData and quest.questData["acNpc"] == entity.npcId:
                            return quest
        return None
