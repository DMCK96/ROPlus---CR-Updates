import roplus
from roplus import fsm

from guis import uiUtils
import BigWorld

import time


class CompleteQuest(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Complete quest ..."
        self.currentQuestCompletor = None
        self.completors = {}

    def needToRun(self):

        p = BigWorld.player()

        if not p or p.life != 1:
            return False

        self.currentQuestCompletor = self.selectQuestCompletor()
        return self.currentQuestCompletor

    def run(self):
        self.bot.currentQuestCompletor = self.currentQuestCompletor
        self.name = "Running quest completor"
        self.currentQuestCompletor.resetActions()
        self.currentQuestCompletor.run()

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
                        return self.bot.getQuestCompletor(questId)

        return None
