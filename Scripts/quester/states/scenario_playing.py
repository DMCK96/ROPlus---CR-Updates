import roplus

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import nav
from roplus.helpers import questing

from helpers.scenario import Scenario
from guis import uiUtils
import BigWorld
import gameglobal

import time

class ScenarioPlaying(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Scenario playing ..."

    def needToRun(self):
        p = BigWorld.player()

        if not p:
            return False

        return gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA

    def run(self):
        scen = Scenario.getInstanceInPlay()
        if scen and scen.canEsc and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            scen.stopPlay()
            self.bot.engine.wait(1)

    def onEnter(self):
        return None

    def onLeave(self):
        return None
