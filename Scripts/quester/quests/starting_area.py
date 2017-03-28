import roplus
import quester
from roplus.helpers import nav
from roplus.helpers import entities
from quester.logics.quest_completor import GenericQuestCompletor

import BigWorld, const
from helpers import qingGong

import time

class TailoredWithCareCompletor(GenericQuestCompletor):

    def run(self):
        if self.useAnyInventoryItems([103111, 103211, 103311, 103411, 103511, 103611]):
            self.bot.engine.wait(2)
            return True
        return GenericQuestCompletor.run(self)

class SparWithAkutaCompletor(GenericQuestCompletor):

    def run(self):
        p = BigWorld.player()
        akuta = entities.findEntityByCharType(23028, 20)
        if akuta and hasattr(akuta, "spellInfo"): # Use this to detect casting :x
            self.state = "Dodge Akuta's attack !"
            nav.stopMove()
            p.faceTo(akuta)
            qingGong.switchToDodge(qingGong.GO_LEFT, p.qinggongMgr)
            self.bot.engine.wait(1)
            return
        GenericQuestCompletor.run(self)

class FortressFirewaterCompletor(GenericQuestCompletor):

    def processQuestGoal(self, goal):
        p = BigWorld.player()
        barrel = entities.findEntityByNpcId(13327, 100)
        if barrel and hasattr(barrel, "attachFx"):
            self.addMarkerNpcToUse(barrel)
            return
        GenericGoalCompletor.processQuestGoal(self, goal)

class SecretSkillCompletor(GenericQuestCompletor):

    def run(self):
        if self.useAnyInventoryItems([232702, 232719, 232678, 232693, 232707, 232686]):
            self.bot.engine.wait(2)
            return
        GenericQuestCompletor.run(self)

# Tell the bot about the custom quest completor
QUEST_COMPLETORS = { 
    13303: TailoredWithCareCompletor,
    13376: SparWithAkutaCompletor,
    13335: FortressFirewaterCompletor,
    13357: SecretSkillCompletor
}