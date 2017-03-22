import roplus
import imgui
import combats

from grinder import settings
import profile_editor

import data
import BigWorld

import inspect

class MainWindow:

    def __init__(self, botInstance):
        self.bot = botInstance
        self.profileEditor = profile_editor.ProfileEditor(botInstance)
        self.visible = False
        self.displayProfileEditor = False
        if self.bot.settings["lastUsedCombat"] in combats.LOADED_COMBATS.keys():
            self.combatSelectedIndex = combats.LOADED_COMBATS.keys().index(self.bot.settings["lastUsedCombat"])
        else:
            self.combatSelectedIndex = -1
        roplus.registerCallback("ROPlus.OnDrawGUI", self.onDrawGuiCallback)

    def show(self):
        self.visible = True

    def onDrawGuiCallback(self, args):
        if self.visible:
            if imgui.begin("Grinder##grinder_mainwindow", (300,350)):
                player = BigWorld.player()
                imgui.columns(2)
                imgui.separator()
                imgui.text("State")
                imgui.nextColumn()
                if self.bot.running and self.bot.engine.currentState:
                    imgui.text(self.bot.engine.currentState.name)
                else:
                    imgui.text("N/A")
                imgui.nextColumn()
                imgui.text("Name")
                imgui.nextColumn()
                if player:
                    imgui.text(player.playerName)
                else:
                    imgui.text("Not ingame")
                imgui.nextColumn()
                imgui.text("Experience")
                imgui.nextColumn()
                if player:
                    exp_label = '{0} / {1}'.format(player.exp, data.avatar_lv_data.data.get(player.realLv, {}).get('upExp', '?'))
                    imgui.text(exp_label)
                else:
                    imgui.text("Not ingame")
                imgui.columns(1)
                imgui.separator()
                if not self.bot.running:
                    if imgui.button("Start##grinder_start_bot", (imgui.getContentRegionAvail()[0] / 2, 25)):
                        try:
                            combat_inst = combats.LOADED_COMBATS[combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]]
                            self.bot.start(combat_inst)
                            self.profileEditor.hide()
                        except IndexError:
                            roplus.log("Please select a combat script first !")
                    imgui.sameLine()
                    if imgui.button("Profile editor##grinder_profile_editor", (imgui.getContentRegionAvail()[0], 25)):
                        self.profileEditor.show()
                else:
                    if imgui.button("Stop##grinder_stop_bot", (imgui.getContentRegionAvail()[0], 25)):
                        self.bot.stop()

                imgui.separator()
                if imgui.button("Save settings##grinder_save_settings", (imgui.getContentRegionAvail()[0], 25)):
                    settings.saveSettings(self.bot.settings, "grinder")
                if imgui.collapsingHeader("Combats##grinder_combats_settings", 0x20):
                    selectedChanged, self.combatSelectedIndex = imgui.combo("##grinder_combatcombo", self.combatSelectedIndex, combats.LOADED_COMBATS.keys())
                    if selectedChanged:
                        self.bot.settings["lastUsedCombat"] = combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]
                        self.bot.saveSettings()
                    imgui.sameLine()
                    if imgui.button("Reload##grinder_reload_scripts", (imgui.getContentRegionAvail()[0], 24)):
                        combats.reloadCombatModules()
                        
        
            imgui.end()