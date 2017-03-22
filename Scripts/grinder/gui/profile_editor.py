import roplus
import imgui

from grinder import profile

import BigWorld

import math
import os

class ProfileEditor:

    def __init__(self, botInstance):
        self.bot = botInstance
        self.visible = False
        roplus.registerCallback("ROPlus.OnDrawGUI", self.onDrawGuiCallback)
        self.availableProfiles = profile.getProfiles()
        self.profilesSelectedIndex = 0
        self.loadProfile(self.bot.settings["lastUsedProfile"])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def saveProfile(self):
        profile.saveProfile(self.bot.currentProfile)
        self.bot.settings["lastUsedProfile"] = self.bot.currentProfile["name"];
        self.bot.saveSettings();
        self.availableProfiles = profile.getProfiles()
        if not self.bot.currentProfile["name"] in self.availableProfiles:
            self.availableProfiles.append(self.bot.currentProfile["name"])
        self.profilesSelectedIndex = self.availableProfiles.index(self.bot.currentProfile["name"])

    def loadProfile(self, name):
        try:
            self.bot.currentProfile = profile.loadProfile(name)
            self.availableProfiles = profile.getProfiles()
            self.bot.settings["lastUsedProfile"] = name;
            self.bot.saveSettings();
            return True
        except Exception:
            return False

    def onDrawGuiCallback(self, args):
        if self.visible:
            if imgui.begin("Grinder - Profile Editor##grinder_profileeditor", (400,400)):
                textChanged, self.bot.currentProfile["name"] = imgui.inputText("##profilesavename", self.bot.currentProfile["name"])
                imgui.sameLine()
                if imgui.button("Save##profileeditor_save_profile"):
                    self.saveProfile()
                selectedChanged, self.profilesSelectedIndex = imgui.combo("##qfsdsfs", self.profilesSelectedIndex, self.availableProfiles)
                imgui.sameLine()
                if imgui.button("Load##profileeditor_load_profile"):
                    profileName = self.availableProfiles[self.profilesSelectedIndex]
                    self.loadProfile(profileName)
                if imgui.button("Clear profile##profileeditor_clear_profile", (imgui.getContentRegionAvail()[0], 25)):
                    self.bot.currentProfile = profile.defaultProfile()
                imgui.separator()
                if imgui.collapsingHeader("Hotspots##profileeditor_hotspots", 0x20):
                    if imgui.button("Add hotspot"):
                        player = BigWorld.player()
                        if player:
                            position = player.position
                            self.bot.currentProfile["hotspots"].append((position.x, position.y, position.z, player.mapID))
                    imgui.sameLine()
                    if imgui.checkbox("Randomize hotspots", self.bot.currentProfile["randomizeHotspots"] ):
                        self.bot.currentProfile["randomizeHotspots"] = not self.bot.currentProfile["randomizeHotspots"]

                    if len(self.bot.currentProfile["hotspots"]) > 0:
                        imgui.columns(3)
                        imgui.text("MapID")
                        imgui.nextColumn()
                        imgui.text("Position")
                        imgui.nextColumn()
                        imgui.text("Action")
                        imgui.nextColumn()
                        hotspotToRemove = None
                        for index, hotspot in enumerate(self.bot.currentProfile["hotspots"]):
                            imgui.text(str(hotspot[3]))
                            imgui.nextColumn()
                            imgui.text(str(math.trunc(hotspot[0])) + ", " + str(math.trunc(hotspot[1])) + ", " + str(math.trunc(hotspot[2])))
                            imgui.nextColumn()
                            if imgui.button("Remove##rem_hotspot" + str(index)):
                                hotspotToRemove = hotspot
                            imgui.nextColumn()
                        if hotspotToRemove:
                            self.bot.currentProfile["hotspots"].remove(hotspotToRemove)
                        imgui.columns(1)
            imgui.end()