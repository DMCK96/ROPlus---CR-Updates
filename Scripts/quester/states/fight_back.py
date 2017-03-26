import roplus
import time

from roplus import fsm
from roplus.helpers import maths

import BigWorld
import helpers.navigator

class FightBack(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Combat"
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
        p = BigWorld.player()
        result = None
        closestDistance = 0
        if p:
            for entity in p.entitiesInRange(maxRange):
                entityDistance = p.position.distTo(entity.position)
                if p.isEnemy(entity) and entity.inCombat and entity.hp > 0 and (result == None or closestDistance > entityDistance):
                    result = entity
                    closestDistance = entityDistance
        return result
