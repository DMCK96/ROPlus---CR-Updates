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
        self.name = "Blademaster"
        self.author = "ROPlus"
        # Init skills
        self.QuickSlash = Skill(1301)
        self.MercilessStrike = Skill(1304)
        self.JuggernautSweep = Skill(1313)
        self.MartialInstinctSecret = Skill(1303)

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

            # Face the target
            if self.handleMove:
                p.faceTo(target)

            if self.MartialInstinctSecret.isKnown() and p.position.distTo(target.position) <= 3.0 and self.MartialInstinctSecret.isUsable():
                self.MartialInstinctSecret.cast(target)
                return

            if self.MercilessStrike.isKnown() and p.position.distTo(target.position) <= 3.0 and self.MercilessStrike.isUsable():
                self.MercilessStrike.cast(target)
                return

            if self.QuickSlash.isKnown() and p.position.distTo(target.position) <= 3.0 and self.QuickSlash.isUsable():
                self.QuickSlash.cast(target)
                return

            if self.JuggernautSweep.isKnown() and p.position.distTo(target.position) <= 3.0 and self.JuggernautSweep.isUsable():
                self.JuggernautSweep.cast(target)
                return