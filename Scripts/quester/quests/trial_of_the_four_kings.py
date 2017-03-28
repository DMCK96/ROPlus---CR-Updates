import roplus
import quester
from roplus.helpers import nav
from roplus.helpers import entities
from quester.logics.quest_completor import GenericQuestCompletor

import BigWorld
from guis import uiConst
from helpers import qingGong

import time

class TrialOfTheFourKingsCompletor(GenericQuestCompletor):

    MONSTERS_TO_KILL = [40701, 40707]
    def run(self):
        p = BigWorld.player()

        # Check if we are in the arena
        if p.inFuben():
            self.skipAutoQuest = True
            self.skipTurnIn = True
            self.skipQuestGoal = True

            trialEnvoy = entities.findEntityByNpcId(41100, 100)
            nextPortal = entities.findEntityByJiguanId(10002, 100)
            cunningHogsheads = filter(lambda e: getattr(e, "charType", 0) == 40702 and (any(getattr(e, "statesClientPub", {})) or any(getattr(e, "statesOld", {}))), entities.getAttackableEntities(100))
            treasureBoxes = filter(lambda e: e.IsBox and getattr(e, "treasureBoxId", 0) == 68 , entities.getEntities(100))
            transports = filter(lambda e: 'Transport' in e.__class__.__name__ , entities.getEntities(100))

            if any(treasureBoxes) and self.moveToEntity(treasureBoxes[0], 3):
                treasureBoxes[0].use()
                self.bot.engine.wait(3)

            if trialEnvoy and self.moveToEntity(trialEnvoy, 3):
                trialEnvoy.cell.executeFbAI(1, uiConst.TRAINING_FUBEN_TYPE_OLD)
                self.bot.engine.wait(3)

            if nextPortal and self.moveToEntity(nextPortal, 3):
                nextPortal.use()
                self.bot.engine.wait(3)

            if any(transports) and self.moveToEntity(transports[0], 1):
                p.cell.exitSingleFuben()
                self.bot.engine.wait(3)

            if any(cunningHogsheads):
                self.addMonsterToAttack(cunningHogsheads[0])

        GenericQuestCompletor.run(self)

# Tell the bot about the custom quest completor
QUEST_COMPLETORS = { 
    22009: TrialOfTheFourKingsCompletor
}