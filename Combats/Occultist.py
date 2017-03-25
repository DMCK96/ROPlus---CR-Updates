# ROPlus stuff
import roplus
from combats import CombatBase
from roplus.helpers.skill import Skill
from roplus.helpers import nav

# Python base
import time

# RO Stuff
import BigWorld


class Combat(CombatBase):
    def __init__(self):
        # Base script informations
        self.name = "Occultist"
        self.author = "ROPlus"
        # Init skills
        self.HellfireClaw = Skill(1602)
        self.CreepingPain = Skill(1603)
        self.DemonsRancor = Skill(1615)
        self.GraspingSpirits = Skill(1604)

    # Called in loop during the combat
    def onCombat(self, target):
        p = BigWorld.player()
        if p and target:

            # Move close to target if needed
            if self.handleMove:
                tDistance = p.position.distTo(target.position)
                if tDistance > 25:
                    nav.moveToPathFind((target.position.x, target.position.y, target.position.z, p.mapID))
                    return
                else:
                    nav.stopMove()

            # If we are already using a skill, no need to go further...
            if p.isUseSkill():
                return

            # Face the target
            if self.handleMove:
                p.faceTo(target)

            if self.DemonsRancor.isKnown() and p.position.distTo(target.position) <= 25.0 and self.DemonsRancor.isUsable():
                self.DemonsRancor.cast(target)
                return

            if self.CreepingPain.isKnown() and p.position.distTo(target.position) <= 25.0 and self.CreepingPain.isUsable():
                self.CreepingPain.cast(target)
                return

            if self.HellfireClaw.isKnown() and p.position.distTo(target.position) <= 25.0 and self.HellfireClaw.isUsable():
                self.HellfireClaw.cast(target)
                return