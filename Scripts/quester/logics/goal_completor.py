import roplus
from roplus.helpers import nav
from roplus.helpers import entities

import gameglobal
import const
import BigWorld
from guis import uiUtils

import time        

###########################################
# GenericGoalCompletor
# Will try to do the goal with automatic game functions
###########################################

class GenericGoalCompletor(object):

    def __init__(self, questCompletor, taskGoal):
        self.name = "Generic goal completor"
        self.quest = questCompletor
        self.lastAutoPathTime = 0
        self.goal = taskGoal
        self.goalTrackId = taskGoal.get(const.QUEST_GOAL_TRACK_ID, '')
        self.goalTrackType = taskGoal.get(const.QUEST_GOAL_TRACK_TYPE, '')
        self.goalType = taskGoal.get(const.QUEST_GOAL_TYPE, '')
        self.goalOrder = taskGoal.get(const.QUEST_GOAL_ORDER, '')

    def getName(self):
        return self.name

    def run(self):
        p = BigWorld.player()

        if p.isDoingAction:
            return

        if self.quest.bot.fightBackState.needToRun():
            self.name = "Fight back"
            self.quest.bot.fightBackState.run()
            return

        if self.goalTrackId and time.time() - self.lastAutoPathTime > 3:
            uiUtils.findPosById(self.goalTrackId)
            self.lastAutoPathTime = time.time()

###########################################
# KillMonsterGoalCompletor
# Goal to kill monsters
###########################################

class KillMonsterGoalCompletor(GenericGoalCompletor):

    def __init__(self, questCompletor, taskGoal, monsters):
        GenericGoalCompletor.__init__(self, questCompletor, taskGoal)
        self.name = "Kill monster goal completor"
        self.monsters = monsters

    def run(self):
        p = BigWorld.player()
        ents = [ ent for ent in entities.getAttackableEntities(30) if ent.charType in self.monsters ]

        if len(ents) > 0:
            target = ents[0]
            self.name = "Attack : " + target.roleName
            self.quest.bot.currentCombat.onCombat(target)
            return

        GenericGoalCompletor.run(self)

###########################################
# UseAnyItemsGoalCompletor
# Attempt to equip any items specified in the list
###########################################

class UseAnyItemsGoalCompletor(GenericGoalCompletor):

    def __init__(self, questCompletor, taskGoal, items):
        GenericGoalCompletor.__init__(self, questCompletor, taskGoal)
        self.name = "Use items goal completor"
        self.items = items

    def run(self):
        p = BigWorld.player()
        for itemId in self.items:
            page, pos = p.realInv.findItemById(itemId)
            if page != const.CONT_NO_POS:
                item = p.realInv.getQuickVal(page, pos)
                p.useBagItem(page, pos)
                self.quest.bot.engine.wait(2)
                roplus.log("Use item : " + str(itemId))
                return

        GenericGoalCompletor.run(self)