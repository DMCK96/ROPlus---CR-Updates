import roplus
from combats import CombatBase
from roplus.helpers.skill import Skill
from roplus.helpers import nav

import time

# RO Stuff
import BigWorld

class Combat(CombatBase):

    def __init__(self):
        # Base script informations
        self.name = "Swordmage"
        self.author = "ROPlus"
        # Init skills
        self.NimbusReign        = Skill(1244)
        self.LightningOrb       = Skill(1202)
        self.SearingWake        = Skill(1204)
        self.AngelFire          = Skill(1203)
        self.LambentBolt        = Skill(1201)

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

            if self.SearingWake.isKnown() and self.SearingWake.isUsable() and p.ammoNum >= 5:
                self.SearingWake.cast(target)
                return

            if self.LightningOrb.isKnown() and self.LightningOrb.isUsable():
                self.LightningOrb.cast(target)
                return

            if self.AngelFire.isKnown() and self.AngelFire.isUsable():
                self.AngelFire.cast(target)
                return

            if self.LambentBolt.isKnown() and self.LambentBolt.isUsable():
                self.LambentBolt.cast(target)
                return