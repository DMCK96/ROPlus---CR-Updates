import roplus
import roplus.helpers.questing

import imgui
import combats

from quester import settings

from guis import uiUtils
import data
import BigWorld
import commQuest

from data import quest_data as QD
from data import seeker_data as SKD

import inspect
import sys

class MainWindow:

    def __init__(self, botInstance):
        self.bot = botInstance
        self.visible = False
        if self.bot.settings["lastUsedCombat"] in combats.LOADED_COMBATS.keys():
            self.combatSelectedIndex = combats.LOADED_COMBATS.keys().index(self.bot.settings["lastUsedCombat"])
        else:
            self.combatSelectedIndex = -1
        roplus.registerCallback("ROPlus.OnDrawGUI", self.onDrawGuiCallback)

    def show(self):
        self.visible = True

    def onDrawGuiCallback(self, args):
        if self.visible:
            if imgui.begin("Quester##Quester_mainwindow", (300,350)):
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
                    imgui.nextColumn()
                else:
                    imgui.text("Not ingame")
                    imgui.nextColumn()
                if self.bot.running and self.bot.currentQuestCompletor:
                    qC = self.bot.currentQuestCompletor;
                    imgui.text("Quest")
                    imgui.nextColumn()
                    imgui.text(str(qC.questName))
                    imgui.nextColumn()
                    imgui.text("Quest ID")
                    imgui.nextColumn()
                    imgui.text(str(qC.questId))
                    imgui.nextColumn()
                    imgui.text("State")
                    imgui.nextColumn()
                    imgui.text(str(qC.state))
                    imgui.nextColumn()
                    if qC.currentGoalCompletor:
                        gC = qC.currentGoalCompletor
                        imgui.text("Goal completor")
                        imgui.nextColumn()
                        imgui.text(gC.getName())
                        imgui.nextColumn()
                imgui.columns(1)
                imgui.separator()

                if not self.bot.running:
                    if imgui.button("Start##Quester_start_bot", (imgui.getContentRegionAvail()[0], 25)):
                        try:
                            combat_inst = combats.LOADED_COMBATS[combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]]
                            self.bot.start(combat_inst)
                        except IndexError:
                            roplus.log("Please select a combat script first !")
                else:
                    if imgui.button("Stop##Quester_stop_bot", (imgui.getContentRegionAvail()[0], 25)):
                        self.bot.stop()

                imgui.separator()
                if imgui.button("Save settings##Quester_save_settings", (imgui.getContentRegionAvail()[0], 25)):
                    settings.saveSettings(self.bot.settings, "Quester")

                #
                # Combats
                #
                if imgui.collapsingHeader("Combats##Quester_combats_settings", 0x20):
                    selectedChanged, self.combatSelectedIndex = imgui.combo("##Quester_combatcombo", self.combatSelectedIndex, combats.LOADED_COMBATS.keys())
                    if selectedChanged:
                        self.bot.settings["lastUsedCombat"] = combats.LOADED_COMBATS.keys()[self.combatSelectedIndex]
                        self.bot.saveSettings()
                    imgui.sameLine()
                    if imgui.button("Reload##Quester_reload_scripts", (imgui.getContentRegionAvail()[0], 24)):
                        combats.reloadCombatModules()

                #
                # Quest Logs
                #
                if imgui.collapsingHeader("Quests Log##Quester_questslog"):
                    if player and player.questInfoCache:
                        for questCategory in player.questInfoCache:
                            for questInfo in roplus.helpers.questing.getQuestInfosFromCache(questCategory):
                                if imgui.treeNode("["+questCategory+"] "+questInfo.getName()+"##" + str(questInfo.questId)):                                
                                    if imgui.treeNode("-> Quest Data##" + str(questInfo.questId)):
                                        for k,v in questInfo.questData.items():
                                            imgui.text(str(k) + " -> " + str(v))
                                        imgui.treePop()
                                    if imgui.treeNode("-> Quest Details##" + str(questInfo.questId)):
                                        for k,v in player.genQuestDetail(questInfo.questId, -1).items():
                                            imgui.text(str(k) + " -> " + str(v))
                                        imgui.treePop()
                                    imgui.treePop()
        
            imgui.end()