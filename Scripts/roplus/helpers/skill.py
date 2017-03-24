import BigWorld
import helpers.cellCmd
import logicInfo

import time

class Skill:

    def __init__(self, skillId):
        self.skillId = skillId
        self.lastCastTime = 0

    def isKnown(self):
        player = BigWorld.player()
        if player:
            return self.skillId in player.skills
        return False

    def getKnownLevel(self):
        player = BigWorld.player()
        if player and self.isKnown():
            return player.skills[self.skillId].level
        return 0

    def getSkillInfo(self):
        player = BigWorld.player()
        if player and self.isKnown():
            skillInfoVal = player.skills[self.skillId]
            return player.getSkillInfo(skillInfoVal.skillId, skillInfoVal.level)
        return 0

    def cast(self, target):
        if time.time() - self.lastCastTime > 0.3:
            helpers.cellCmd.useSkill(self.skillId, self.getKnownLevel(), target)
            self.lastCastTime = time.time()

    def isOnCooldown(self):
        return logicInfo.isSkillCooldowning(self.skillId)

    def isUsable(self):
        return logicInfo.isUseableSkill(self.skillId)
        