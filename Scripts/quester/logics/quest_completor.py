import roplus

from quester import custom_quests
from quester.logics.goal_completor import GenericGoalCompletor
from quester.logics.goal_completor import KillMonsterGoalCompletor

from roplus.helpers import nav
from roplus.helpers import entities

import BigWorld
import commQuest
import const
from guis import uiUtils
from data import quest_data as QuestData

import time

class QuestCompletor(object):

    def __init__(self, botInstance, questId):
        self.currentGoalCompletor = None
        self.bot = botInstance
        self.questId = questId
        self.state = "Idle"
        self.questData = QuestData.data.get(questId, {})
        self.questName = self.questData.get("name", "")
        self.completors = {}
        self.lastAutoPathTime = 0

    def canRun(self):
        return True

    def run(self):
        self.state = "Idle"
        p = BigWorld.player()
        if commQuest.completeQuestCheck(p, self.questId):
            self.state = "Turn in quest ..."
            # Complete the quest
            completeNpcId = self.questData.get("compNpc", 0)
            completeNpcTask = self.questData.get("comNpcTk", 0)
            if completeNpcId and completeNpcTask:
                completeNpc = entities.findEntityByNpcId(completeNpcId, 3)
                if completeNpc:
                    nav.stopMove()
                    completeNpc.completeQuest(self.questId, {})
                    self.bot.engine.wait(2)
                elif time.time() - self.lastAutoPathTime > 2:
                    uiUtils.findPosById(completeNpcTask)
                    self.lastAutoPathTime = time.time()
        else:
            # Use a quest goal completorCompletor
            goalCompletor = self.selectGoalCompletor()

            if goalCompletor and self.currentGoalCompletor != goalCompletor:
                roplus.log("Using goal completor : " + goalCompletor.name)

            self.currentGoalCompletor = goalCompletor
            if self.currentGoalCompletor:
                self.currentGoalCompletor.run()
            self.state = "Running goal completor ..."

    def selectGoalCompletor(self):
        p = BigWorld.player()
        # Use quest goal completor
        for i, taskGoal in enumerate(self.getGoals()):
            goalState = taskGoal.get(const.QUEST_GOAL_STATE, '')
            goalTrackId = taskGoal.get(const.QUEST_GOAL_TRACK_ID, 0)
            goalOrder = taskGoal.get(const.QUEST_GOAL_ORDER, '')
            if not goalState:
                # Use an already cached completor
                if i in self.completors:
                    return self.completors[i]

                # Use a custom completor
                if (self.questId, goalTrackId) in custom_quests.CUSTOM_QUEST_GOALS_COMPLETORS:
                    self.completors[i] = custom_quests.CUSTOM_QUEST_GOALS_COMPLETORS[(self.questId, goalTrackId)](self, taskGoal)
                    return self.completors[i]                            
                    
                # Use KillMonsterGoalCompletor
                if goalOrder == "needMonsters" and len(self.questData.get("needMonsters", [])) > 0:
                    monstersId = []
                    for monsterDropItem in self.questData["needMonsters"]:
                        monstersId.append(monsterDropItem[0])
                    self.completors[i] = KillMonsterGoalCompletor(self, taskGoal, monstersId)
                    return self.completors[i]
                    
                # Use KillMonsterGoalCompletor
                if goalOrder == "compItemCollect" and len(self.questData.get("monsterDropItems", [])) > i:
                    monstersId = []
                    for monsterDropItem in self.questData["monsterDropItems"]:
                        monstersId.append(monsterDropItem[1])
                    self.completors[i] = KillMonsterGoalCompletor(self, taskGoal, monstersId)
                    return self.completors[i]
                    
                # Use KillMonsterGoalCompletor
                if goalOrder == "beatMonsterNo" and self.questData.get("beatMonsterNo", ''):
                    monsterId = self.questData["beatMonsterNo"]
                    self.completors[i] = KillMonsterGoalCompletor(self, taskGoal, [monsterId])
                    return self.completors[i]

                # Use GenericGoalCompletor
                self.completors[i] = GenericGoalCompletor(self, taskGoal)
                return self.completors[i]

        return None

    def getGoals(self):
        results = ()
        p = BigWorld.player()
        if p:
            questDetail = p.genQuestDetail(self.questId, -1)
            results = (questDetail.get("taskGoal", []))
        return results
