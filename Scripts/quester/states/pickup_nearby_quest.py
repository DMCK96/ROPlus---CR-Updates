import roplus

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import nav
from roplus.helpers import questing
from roplus.helpers import entities

from data import quest_data as QuestData
from guis import uiUtils
import BigWorld

import time

class PickupNearbyQuest(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "PickupNearbyQuest"
        self.lastTaskRunTime = 0
        self.currentQuest = {}

    def needToRun(self):
        p = BigWorld.player()
        if not p or p.isDoingAction or p.hp <= 0:
            return False
        questId = self.chooseQuest()
        if questId:
            self.currentQuestId = questId
            self.currentQuestData = QuestData.data.get(questId, {})
            return True

    def run(self):
        p = BigWorld.player()
        pickupNpcId = self.currentQuestData["acNpc"]
        pickupNpcTask = self.currentQuestData["acNpcTk"]
        pickupNpc = entities.findEntityByNpcId(pickupNpcId)

        if pickupNpc:
            if p.position.distTo(pickupNpc.position) > 2:
                self.name = "Moving to pickup quest : " + self.currentQuestData.get("name", "")
                nav.moveToPathFind((pickupNpc.position.x, pickupNpc.position.y, pickupNpc.position.z, p.mapID))
                return
            else:
                self.name = "Pickup quest : " + self.currentQuestData.get("name", "")
                nav.stopMove()
                pickupNpc.acceptQuest(self.currentQuestId)
                self.bot.engine.wait(1)
                return

        if time.time() - self.lastTaskRunTime > 2:
            uiUtils.findPosById(pickupNpcTask)
            self.lastTaskRunTime = time.time()
            self.name = "Moving to pickup quest : " + self.currentQuestData.get("name", "")
            return

    def onEnter(self):
        return None

    def onLeave(self):
        return None

    def chooseQuest(self):
        p = BigWorld.player()
        if not p or not p.questInfoCache:
            return None
        availableQuests = {}
        for questId in p.questInfoCache["available_tasks"]:
            questData = QuestData.data.get(questId, {})
            if questData and "acNpc" in questData and "acNpcTk" in questData:
                availableQuests[questId] = questData
        for questId, questData in availableQuests.items():
            for entity in p.entitiesInRange(1000):
                if getattr(entity, "npcId", -1) == questData["acNpc"]:
                    return questId
