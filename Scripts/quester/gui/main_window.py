import roplus
import roplus.helpers.questing
from roplus.helpers.questing import QuestGoal

import imgui
import combats

from quester import settings

from guis import uiUtils
import data
import BigWorld
import commQuest

from data import quest_data as QuestData
from data import seeker_data as SeekerData

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
        p = BigWorld.player()
        if self.visible:
            if imgui.begin("Quester##Quester_mainwindow", (300,350)):
                imgui.columns(2)
                imgui.separator()
                imgui.text("Name")
                imgui.nextColumn()
                if p:
                    imgui.text(p.playerName)
                else:
                    imgui.text("Not ingame")
                imgui.nextColumn()
                imgui.text("Map ID")
                imgui.nextColumn()
                if p:
                    imgui.text(str(p.mapID))
                else:
                    imgui.text("Not ingame")
                imgui.nextColumn()
                imgui.text("Experience")
                imgui.nextColumn()
                if p:
                    exp_label = '{0} / {1}'.format(p.exp, data.avatar_lv_data.data.get(p.realLv, {}).get('upExp', '?'))
                    imgui.text(exp_label)
                    imgui.nextColumn()
                else:
                    imgui.text("Not ingame")
                    imgui.nextColumn()
                imgui.text("State")
                imgui.nextColumn()
                if self.bot.running and self.bot.engine.currentState:
                    imgui.text(self.bot.engine.currentState.name)
                else:
                    imgui.text("N/A")
                imgui.nextColumn()
                imgui.text("Active quest")
                imgui.nextColumn()
                if self.bot.running and self.bot.currentQuestCompletor:
                    imgui.text(str(self.bot.currentQuestCompletor.questId))
                else:
                    imgui.text("N/A")
                imgui.nextColumn()
                imgui.text("Quest state")
                imgui.nextColumn()
                if self.bot.running and self.bot.currentQuestCompletor:
                    imgui.text(self.bot.currentQuestCompletor.state)
                else:
                    imgui.text("N/A")
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
                if imgui.collapsingHeader("[Debug] Quests Info##Quester_questslog"):
                    if p and p.questInfoCache:
                        for category, questIds in p.questInfoCache.items():
                            if imgui.treeNode("[{}] {}".format(str(len(questIds)), category)):
                                for questId in questIds:
                                    questDetails = p.genQuestDetail(questId, -1)
                                    questData = QuestData.data.get(questId, {})
                                    if questData and imgui.treeNode("[{}] {}".format(str(questId), questData.get("name", ""))):
                                        if questDetails and questDetails.get("taskGoal", {}) and imgui.treeNode("Quest goals ({})##questid_{}".format(str(len(questDetails["taskGoal"])), str(questId))):
                                            for i, taskGoal in enumerate(questDetails["taskGoal"]):
                                                questGoal = QuestGoal(taskGoal)
                                                if imgui.treeNode("[{0}] {1}##quest_goal_{2}_{0}".format(str(i+1), questGoal.description, str(questId))):
                                                    imgui.text("State : {}".format(str(questGoal.state)))
                                                    imgui.text("Type : {}".format(str(questGoal.type)))
                                                    imgui.text("Track Seek ID : {}".format(str(questGoal.trackSeekId)))
                                                    imgui.text("Track Task Type : {}".format(str(questGoal.trackTaskType)))
                                                    imgui.text("Order : {}".format(str(questGoal.order)))
                                                    if questGoal.trackSeekData and imgui.treeNode("Track Task data##questid_{}_{}".format(str(questId), str(i))):
                                                        for k,v in questGoal.trackSeekData.items():
                                                            imgui.text("{} -> {}".format(str(k), str(v)))
                                                        imgui.treePop()
                                                    imgui.treePop()
                                            imgui.treePop()
                                        if questData and imgui.treeNode("Quest data##questid_{}".format(str(questId))):
                                            for k,v in questData.items():
                                                imgui.text("{} -> {}".format(str(k), str(v)))
                                            imgui.treePop()
                                        if questDetails and imgui.treeNode("Quest details##questid_{}".format(str(questId))):
                                            for k,v in questDetails.items():
                                                imgui.text("{} -> {}".format(str(k), str(v)))
                                            imgui.treePop()
                                        imgui.treePop()
                                imgui.treePop()
                            #for questInfo in roplus.helpers.questing.getQuestInfosFromCache(questCategory):
                            #    if imgui.treeNode("["+questCategory+"] "+questInfo.getName()+"##" + str(questInfo.questId)):
                            #        if imgui.treeNode("-> Quest Data##" + str(questInfo.questId)):
                            #            for k,v in questInfo.questData.items():
                            #                imgui.text(str(k) + " -> " + str(v))
                            #            imgui.treePop()
                            #        if imgui.treeNode("-> Quest Details##" + str(questInfo.questId)):
                            #            for k,v in player.genQuestDetail(questInfo.questId, -1).items():
                            #                imgui.text(str(k) + " -> " + str(v))
                            #            imgui.treePop()
                            #        imgui.treePop()
        
            imgui.end()