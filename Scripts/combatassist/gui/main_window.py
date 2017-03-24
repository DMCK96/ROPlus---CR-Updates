import roplus
import imgui
import combats

import data
import BigWorld

import inspect

class MainWindow:

    def __init__(self):
        self.visible = False
        self.rotationEnabled = False
        self.combatCheck = True
        self.handleMovements = False
        self.autoTargetEnemies = False
        #if self.bot.settings["lastUsedCombat"] in combats.LOADED_COMBATS.keys():
        #    self.combatSelectedIndex = combats.LOADED_COMBATS.keys().index(self.bot.settings["lastUsedCombat"])
        #else:
        #    self.combatSelectedIndex = -1
        self.combatSelectedIndex = -1
        self.combatRotationName = None
        roplus.registerCallback("ROPlus.OnDrawGUI", self.onDrawGuiCallback)
        roplus.registerCallback("ROPlus.OnPulse", self.onPulseCallback)

    def show(self):
        self.visible = True

    def onDrawGuiCallback(self, args):
        if self.visible:
            if imgui.begin("Combat Assist##combatassist_mainwindo", (450,300)):
                player = BigWorld.player()

                imgui.text("Combat script : ")
                selectedChanged, self.combatSelectedIndex = imgui.combo("##combatassist_combatcombo", self.combatSelectedIndex, combats.LOADED_COMBATS.keys())
                if selectedChanged:
                    combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]
                    self.combatRotationName = combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]
                    roplus.log("Using combat script : " + self.combatRotationName)
                imgui.sameLine()
                if imgui.button("Reload##grinder_reload_scripts", (imgui.getContentRegionAvail()[0], 24)):
                    combats.reloadCombatModules()
                imgui.separator()
                if self.combatSelectedIndex == -1:
                    imgui.text("Select a combat script first ...")
                else:
                    if imgui.checkbox("Enable combat", self.rotationEnabled):
                        self.rotationEnabled = not self.rotationEnabled
                    if imgui.checkbox("Only attack in combat targets", self.combatCheck):
                        self.combatCheck = not self.combatCheck
                    if imgui.checkbox("Allow combat script to use movements", self.handleMovements):
                        self.handleMovements = not self.handleMovements
                    if imgui.checkbox("Automatically target attackers (Not implemented)", self.autoTargetEnemies):
                        self.autoTargetEnemies = not self.autoTargetEnemies
            imgui.end()

    def onPulseCallback(self, args):
        p = BigWorld.player()
        if p and self.rotationEnabled and self.combatRotationName and self.combatRotationName in combats.LOADED_COMBATS:
            combatInst = combats.LOADED_COMBATS[self.combatRotationName]
            t = p.targetLocked
            if t and p.canBeAttack(t) and (t.inCombat or not self.combatCheck):
                combatInst.handleMove = self.handleMovements
                combatInst.onCombat(t)