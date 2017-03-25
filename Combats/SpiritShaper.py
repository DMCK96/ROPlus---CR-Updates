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
        self.name = "SpiritShaper"
        self.author = "ROPlus"
        # Init skills
        self.MionideBells = Skill(1401)
        self.SpectralMagpie = Skill(1402)
        self.FireflyHex = Skill(1406)
        self.EssenceOfSpring = Skill(1411)

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


            if self.FireflyHex.isKnown() and p.position.distTo(target.position) <= 25.0 and self.FireflyHex.isUsable():
                self.FireflyHex.cast(target)
                return

            if self.SpectralMagpie.isKnown() and p.position.distTo(target.position) <= 25.0 and self.SpectralMagpie.isUsable():
                self.SpectralMagpie.cast(target)
                return

            if self.EssenceOfSpring.isKnown() and self.EssenceOfSpring.isUsable():
                self.EssenceOfSpring.cast(p)
                return

            if self.MionideBells.isKnown() and p.position.distTo(target.position) <= 25.0 and self.MionideBells.isUsable():
                self.MionideBells.cast(target)
                return
