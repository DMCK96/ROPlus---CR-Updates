import roplus
import quester
from roplus.helpers import nav
from roplus.helpers import entities
from quester.logics.quest_completor import QuestCompletor
from quester.logics.goal_completor import GenericGoalCompletor
from quester.logics.goal_completor import UseAnyItemsGoalCompletor

import BigWorld
from helpers import qingGong

import time

class TailoredWithCareEquipItems(UseAnyItemsGoalCompletor):

    def __init__(self, questCompletor, taskGoal):
        UseAnyItemsGoalCompletor.__init__(self, questCompletor, taskGoal, [103111, 103211, 103311, 103411, 103511, 103611])

class SecretSkill(UseAnyItemsGoalCompletor):

    def __init__(self, questCompletor, taskGoal):
        UseAnyItemsGoalCompletor.__init__(self, questCompletor, taskGoal, [232702, 232719, 232678, 232693, 232707, 232686])

class FightAkutaGoalCompletor(GenericGoalCompletor):

    def __init__(self, questCompletor, taskGoal):
        GenericGoalCompletor.__init__(self, questCompletor, taskGoal)
        self.name = "Fight Akuta completor"

    def run(self):
        p = BigWorld.player()
        akuta = entities.findEntityByCharType(23028, 30)

        if akuta:
            if hasattr(akuta, "spellInfo"): # Use this to detect casting :x
                nav.stopMove()
                p.faceTo(akuta)
                qingGong.switchToDodge(qingGong.GO_LEFT, p.qinggongMgr)
                self.quest.bot.engine.wait(2)
            else:
                self.quest.bot.currentCombat.onCombat(akuta)
            return

        GenericGoalCompletor.run(self)

class FortressFirewaterCompletor(GenericGoalCompletor):

    def __init__(self, questCompletor, taskGoal):
        GenericGoalCompletor.__init__(self, questCompletor, taskGoal)
        self.name = "Fortress Firewater Completor"

    def run(self):
        p = BigWorld.player()
        barrel = entities.findEntityByNpcId(13327, 100)

        if p.isDoingAction:
            return

        if barrel:
            if p.position.distTo(barrel.position) > 2:
                self.name = "Move to barrel ..."
                nav.moveToEntityPathFind(barrel)
            else:
                self.name = "Use barrel ..."
                p.useMarkerNpc(barrel.npcId)
            return

        GenericGoalCompletor.run(self)

# Tell the bot about the custom quest completor
QUEST_GOAL_COMPLETORS = { 
    (13303, 00000000): TailoredWithCareEquipItems,
    (13335, 10013254): FortressFirewaterCompletor,
    (13357, 00000000): SecretSkill,
    (13376, 10013247): FightAkutaGoalCompletor
}