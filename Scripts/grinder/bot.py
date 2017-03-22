import roplus

import profile
import settings
import states.combat
import states.roaming
from gui import main_window
from roplus import fsm
import settings

class Bot:

    def __init__(self):
        self.loadSettings()
        self.currentCombat = None
        self.currentProfile = profile.defaultProfile()
        self.engine = fsm.Engine()
        self.running = False
        self.mainWindow = main_window.MainWindow(self)
        self.mainWindow.show()
        roplus.registerCallback("ROPlus.OnPulse", self.onPulseCallback)

    def saveSettings(self):
        settings.saveSettings(self.settings, "grinder")

    def loadSettings(self):
        self.settings = settings.loadSettings("grinder")

    def start(self, combatInst):
        if self.running:
            roplus.log("Bot is already running !")
            return

        if not combatInst:
            roplus.log("Error : No combat script !")
            return

        self.currentCombat = combatInst
        self.currentCombat.handleMove = True

        if not self.currentProfile:
            roplus.log("Error : No profile loaded !")
            return

        if len(self.currentProfile["hotspots"]) < 3:
            roplus.log("Error : profile require at least 3 hotspots !")
            return
            
        self.engine = fsm.Engine()
        self.engine.states.append(states.combat.Combat(self))
        self.engine.states.append(states.roaming.Roaming(self))

        self.running = True
        roplus.log("Bot started !")

    def stop(self):
        if not self.running:
            roplus.log("Bot is not running !")
            return
        self.running = False
        roplus.log("Bot stopped !")

    def onPulseCallback(self, args):
        if self.running:
            self.engine.pulse()