import roplus
import time

from roplus import fsm
from roplus.helpers import maths

import BigWorld
import helpers.navigator

class Combat(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Combat"
        self.combatEntity = None

    def needToRun(self):
        player = BigWorld.player()
        if not player:
            return False

        self.combatEntity = self.getBestAttackTarget(self.bot.settings["combats"]["attackRange"])
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
        player = BigWorld.player()
        result = None
        closestDistance = 0
        if player:
            for entity in player.entitiesInRange(maxRange):
                entityDistance = maths.getDistance3D(player.position, entity.position)
                if entity.IsMonster and entity.canSelected() and entity.hp > 0 and (result == None or closestDistance > entityDistance):
                    result = entity
                    closestDistance = entityDistance
        return result
