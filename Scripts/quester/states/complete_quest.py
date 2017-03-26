import roplus

from roplus import fsm
from roplus.helpers import maths
from roplus.helpers import nav
from roplus.helpers import questing

from quester.logics.quest_completor import QuestCompletor

from guis import uiUtils
import BigWorld

import time

class CompleteQuest(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Complete quest ..."
        self.currentQuest = None
        self.completors = {}

    def needToRun(self):

        p = BigWorld.player()

        if not p or p.life != 1:
            return False

        self.currentQuest = self.selectQuestCompletor()
        return self.currentQuest

    def run(self):
        self.bot.currentQuestCompletor = self.currentQuest
        self.name = "Running quest completor"
        self.currentQuest.run()


    def onEnter(self):
        return None

    def onLeave(self):
        return None

    def selectQuestCompletor(self):
        AUTHORIZED_CATEGORIES = ["complete_tasks", "unfinished_tasks"]
        p = BigWorld.player()
        if p and hasattr(p, "questInfoCache"):
            for category, quests in p.questInfoCache.items():
                if category in AUTHORIZED_CATEGORIES:
                    for questId in quests:
                        completor = None
                        if questId in self.completors:
                            completor = self.completors[questId]
                        else:
                            self.completors[questId] = QuestCompletor(self.bot, questId)

                        if self.completors[questId].canRun():
                            return self.completors[questId]
        return None
