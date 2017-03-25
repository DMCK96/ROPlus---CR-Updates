# ROPlus stuff
import roplus
from combats import CombatBase
from roplus.helpers.skill import Skill
from roplus.helpers import nav

# Python base
import time

# RO Stuff
import BigWorld
import helpers.cellCmd


class Combat(CombatBase):
    def __init__(self):
        # Base script informations
        self.name = "Vanguard"
        self.author = "ROPlus"
        # Init skills
        self.HeroicStrike = Skill(1101)
        self.TornadoSweep = Skill(1104)
        self.BrokenArray = Skill(1105)
        self.ConquerorSweep = Skill(1103)

    # Called in loop during the combat
    def onCombat(self, target):
        p = BigWorld.player()
        if p and target:

            # Move close to target if needed
            if self.handleMove:
                tDistance = p.position.distTo(target.position)
                if tDistance > 3:
                    nav.moveToPathFind((target.position.x, target.position.y, target.position.z, p.mapID))
                    return
                else:
                    nav.stopMove()

            # If we are already using a skill, no need to go further...
            if p.isUseSkill():
                return

            roplus.log("aaaa", time.time())
            helpers.cellCmd.castChargeSkill()

            # Face the target
            if self.handleMove:
                p.faceTo(target)

            if self.ConquerorSweep.isKnown() and p.position.distTo(target.position) <= 3.0 and self.ConquerorSweep.isUsable():
                self.ConquerorSweep .cast(target)
                return

            if self.TornadoSweep.isKnown() and p.position.distTo(target.position) <= 3.0 and self.TornadoSweep.isUsable():
                self.TornadoSweep.cast(target)
                return

            if self.HeroicStrike.isKnown() and p.position.distTo(target.position) <= 3.0 and self.HeroicStrike.isUsable():
                self.HeroicStrike.cast(target)
                return