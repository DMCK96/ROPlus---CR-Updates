import roplus
import time

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import entities

import BigWorld
import helpers.navigator

class FightBack(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Fight Back"
        self.combatEntity = None

    def needToRun(self):
        player = BigWorld.player()
        if not player:
            return False

        self.combatEntity = self.getBestAttackTarget(30)
        return self.combatEntity and player != None and player.hp > 0

    def run(self):
        player = BigWorld.player()
        if player.targetLocked != self.combatEntity:
            player.lockTarget(self.combatEntity)
        self.bot.currentCombat.onCombat(self.combatEntity)

    def onEnter(self):
        return None

    def onLeave(self):
        return None

    def getBestAttackTarget(self, maxRange):
        targets = [ ent for ent in entities.getAttackableEntities(30) if ent.inCombat ]

        if self.combatEntity in targets:
            return self.combatEntity

        if len(targets) > 0:
            return targets[0]

        return None
