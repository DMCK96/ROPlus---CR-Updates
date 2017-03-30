import roplus

from roplus.helpers import nav
from roplus.helpers import entities
from roplus.helpers.questing import QuestGoal

import Math
import gameglobal
import BigWorld
import commQuest
import const
from guis import uiUtils
from data import quest_data as QuestData
from data import quest_npc_data as QuestNpcData
from data import seeker_data as SeekerData
from data import puzzle_data as PuzzleData

import time

class GenericQuestCompletor(object):

    def __new__(cls, botInstance, questId):
        o = super(GenericQuestCompletor, cls).__new__(cls)
        o.bot = botInstance
        o.questId = questId
        o.questData = QuestData.data.get(questId, {})
        o.lastAutoPathTime = 0
        o.resetActions()
        return o

    def resetActions(self):
        self.state = "Idle"
        self.skipTurnIn = False
        self.skipAutoQuest = False
        self.skipQuestGoal = False
        self.monstersToAttack = []
        self.markerNpcsToUse = []
        self.debateNpcsToUse = []
        self.pendingMoveToEntity = None
        self.pendingMoveToEntityDistance = 1

    def addMonsterToAttack(self, monster):
        self.monstersToAttack.insert(0, monster)

    def addMarkerNpcToUse(self, markerNpc):
        self.markerNpcsToUse.insert(0, markerNpc)

    def addDebateNpcTouse(self, debateNpc):
        self.debateNpcsToUse.insert(0, debateNpc)

    def moveToEntity(self, entity, distance=1.0):
        p = BigWorld.player()
        if p.position.distTo(entity.position) < distance:
            return True
        self.pendingMoveToEntity = entity
        self.pendingMoveToEntityDistance = distance
        return False

    def isQuestComplete(self):
        p = BigWorld.player()
        return p and commQuest.completeQuestCheck(p, self.questId)

    def getCompleteNpcId(self):
        return self.questData.get("compNpc", 0)

    def getCompleteNpcTask(self):
        return self.questData.get("comNpcTk", 0)

    def getQuestGoals(self):
        results = []
        p = BigWorld.player()
        if p:
            for taskGoal in p._genQuestGoal(self.questId):
                results.append(QuestGoal(taskGoal))
        return results

    def run(self):
        p = BigWorld.player()

        if p.isDoingAction:
            self.state = "Action in progress ..."
            return True

        # Attempt to parse and process incomplete quest goals
        mainQuestGoal = None
        for questGoal in self.getQuestGoals():
            if not questGoal.state:
                if not self.skipQuestGoal:
                    self.processQuestGoal(questGoal)
                if not mainQuestGoal:
                    mainQuestGoal = questGoal

        # Attempt to solve a puzzle if any
        if self.processPuzzle():
            return True

        # First kill monsters from quest goals
        if self.runAttackMonsters(self.monstersToAttack):
            return True

        # Attempt to kill monsters that attack player
        if self.runAttackMonsters(filter(lambda unit: unit.inCombat and unit.lockedId == p.id, entities.getAttackableEntities(40))):
            return True

        # Attempt to kill monsters that belong to player
        if self.runAttackMonsters(filter(lambda unit: unit.inCombat and unit.belongName == p.roleName, entities.getAttackableEntities(40))):
            return True

        # Attempt to use debate npcs from quest goals
        if self.runDebateNpcs(self.debateNpcsToUse):
            return True

        # Attempt to use marker npcs from quest goals
        if self.runUseMarkerNpcs(self.markerNpcsToUse):
            return True

        # Move to entity
        if self.pendingMoveToEntity:
            self.state = "Move to " + self.pendingMoveToEntity.roleName
            if p.position.distTo(self.pendingMoveToEntity.position) > self.pendingMoveToEntityDistance:
                if time.time() - self.lastAutoPathTime > 2:
                    nav.moveToEntityPathFind(self.pendingMoveToEntity)
                    self.lastAutoPathTime = time.time()
            else:
                nav.stopMove()
            return True

        # If any quest goal task is available, run it
        if mainQuestGoal and mainQuestGoal.trackSeekId and not self.skipAutoQuest:
            trackDestination = nav.getDestinationBySeekId(mainQuestGoal.trackSeekId)
            self.state = "Run automatic task : " + str(mainQuestGoal.trackSeekId)
            if trackDestination and p.position.distTo(Math.Vector3(trackDestination[0], trackDestination[1], trackDestination[2])) > 3:
                nav.moveToPathFind(trackDestination)
            elif time.time() - self.lastAutoPathTime > 2:
                uiUtils.findPosById(mainQuestGoal.trackSeekId)
                self.lastAutoPathTime = time.time()
            return True

        # Finally, complete the quest :D
        if not self.skipTurnIn and self.isQuestComplete():
            self.runTurnInQuest()
            return True

    def runAttackMonsters(self, monsters):
        if any(monsters):
            p = BigWorld.player()
            monsterToAttack = sorted(monsters, key=lambda unit: p.position.distTo(unit.position))[0]
            if p.position.distTo(monsterToAttack.position) < 20:
                self.state = "Attack : " + monsterToAttack.roleName
                self.bot.currentCombat.onCombat(monsterToAttack)
            else:
                self.state = "Approach to attack : " + monsterToAttack.roleName
                if time.time() - self.lastAutoPathTime > 2:
                    nav.moveToEntityPathFind(monsterToAttack)
            return True

    def runUseMarkerNpcs(self, npcs):
        if any(npcs):
            p = BigWorld.player()
            markerNpcToUse = sorted(npcs, key=lambda npc: p.position.distTo(npc.position))[0]
            if p.position.distTo(markerNpcToUse.position) < 3:
                self.state = "Use marker npc : " + markerNpcToUse.roleName
                p.useMarkerNpc(markerNpcToUse.npcId)
                self.bot.engine.wait(1)
            else:
                self.state = "Approach to use : " + markerNpcToUse.roleName
                if time.time() - self.lastAutoPathTime > 2:
                    nav.moveToEntityPathFind(markerNpcToUse)
            return True

    def runDebateNpcs(self, npcs):
        if any(npcs):
            p = BigWorld.player()
            debateNpcToUse = sorted(npcs, key=lambda npc: p.position.distTo(npc.position))[0]
            if p.position.distTo(debateNpcToUse.position) < 3:
                self.state = "Use debate npc : " + debateNpcToUse.roleName
                p.cell.onQuestDebate(self.questId, 1)
                self.bot.engine.wait(1)
            else:
                self.state = "Approach to use : " + debateNpcToUse.roleName
                if time.time() - self.lastAutoPathTime > 2:
                    nav.moveToEntityPathFind(debateNpcToUse)
            return True

    def processPuzzle(self):
        p = BigWorld.player()
        puzzleProxy = gameglobal.rds.ui.puzzle
        if puzzleProxy and puzzleProxy.puzzleId and puzzleProxy.questId == self.questId and puzzleProxy.puzzleInfo:
            puzzleData = PuzzleData.data.get(puzzleProxy.puzzleId, {})
            rightAnswer = puzzleData.get("rightAnswer", None)
            if rightAnswer is not None:
                roplus.log("Found a quest puzzle, answer index : " + str(rightAnswer))
                p.cell.onQuestPuzzle(puzzleProxy.questId, puzzleProxy.puzzleId, rightAnswer)
                self.bot.engine.wait(2)
                return True


    def processQuestGoal(self, goal):
        p = BigWorld.player()
        if goal.order == "compItemCollect":
            for item in self.questData.get("monsterDropItems", []):
                itemId = item[0]
                monsterId = item[1]
                for unit in filter(lambda unit: unit.charType == monsterId, entities.getAttackableEntities(30)):
                    self.addMonsterToAttack(unit)

        if goal.order == "beatMonsterNo":
            beatMonsterNo = self.questData.get("beatMonsterNo", 0)
            for unit in filter(lambda unit: unit.charType == beatMonsterNo, entities.getAttackableEntities(30)):
                self.addMonsterToAttack(unit)

        if goal.order == "needMonsters":
            for item in self.questData.get("needMonsters", []):
                monsterId = item[0]
                needCount = item[1]
                for unit in filter(lambda unit: unit.charType == monsterId, entities.getAttackableEntities(30)):
                    self.addMonsterToAttack(unit)

        if goal.order == "markerNpcs":
            if goal.trackSeekData.get("type", "") == "npc":
                npcId = goal.trackSeekData.get("npcId", 0)
                npc = entities.findEntityByNpcId(npcId, maxRange=30)
                if npc:
                    self.addMarkerNpcToUse(npc)

        if goal.order == "debateNpc":
            if goal.trackSeekData.get("type", "") == "npc":
                npcId = goal.trackSeekData.get("npcId", 0)
                npc = entities.findEntityByNpcId(npcId, maxRange=30)
                if npc:
                    self.addDebateNpcTouse(npc)

    def runTurnInQuest(self):
        p = BigWorld.player()
        completeNpcId = self.getCompleteNpcId()
        completeNpcTask = self.getCompleteNpcTask()

        if completeNpcId and completeNpcTask:
            completeNpc = entities.findEntityByNpcId(completeNpcId)
            if completeNpc and p.position.distTo(completeNpc.position) < 3:
                self.state = "Turn in quest ..."
                nav.stopMove()
                completeNpc.completeQuest(self.questId, {})
                self.bot.engine.wait(2)
            else:
                self.state = "Going to turn in quest ..."
                seekDestination = nav.getDestinationBySeekId(completeNpcTask)
                if seekDestination and p.position.distTo(Math.Vector3(seekDestination[0], seekDestination[1], seekDestination[2])) > 3:
                    nav.moveToPathFind(seekDestination)
                elif time.time() - self.lastAutoPathTime > 2:
                    uiUtils.findPosById(completeNpcTask)
                    self.lastAutoPathTime = time.time()

    def useAnyInventoryItems(self, items):
        p = BigWorld.player()
        for itemId in items:
            page, pos = p.realInv.findItemById(itemId)
            if page != const.CONT_NO_POS:
                p.useBagItem(page, pos)
                roplus.log("Use quest item : " + str(itemId))
                return True