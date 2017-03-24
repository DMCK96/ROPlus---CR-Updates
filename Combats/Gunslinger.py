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
        self.name = "Gunslinger"
        self.author = "ROPlus"
        # Init skills
        self.ThunderShell       = Skill(1501)
        self.HellfireSalvo      = Skill(1502)
        self.ConcussionBomb     = Skill(1503)
        self.OblivionBomb       = Skill(1504)
        self.Grenade            = Skill(1516)

    # Called in loop during the combat
    def onCombat(self, target):
        p = BigWorld.player()
        if p and target:

            # Move close to target if needed
            if self.handleMove:
                tDistance = p.position.distTo(target.position)
                if tDistance > 20:
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

            if self.HellfireSalvo.isKnown() and self.HellfireSalvo.isUsable():
                self.HellfireSalvo.cast(target)
                return

            if self.Grenade.isKnown() and self.Grenade.isUsable():
                self.Grenade.cast(target)
                return

            if self.OblivionBomb.isKnown() and self.OblivionBomb.isUsable():
                self.OblivionBomb.cast(target)
                return

            if self.ConcussionBomb.isKnown() and self.ConcussionBomb.isUsable():
                self.ConcussionBomb.cast(target)
                return

            if self.ThunderShell.isKnown() and self.ThunderShell.isUsable():
                self.ThunderShell.cast(target)
                return