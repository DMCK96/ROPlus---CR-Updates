import BigWorld
import helpers.cellCmd
import commQuest

from data import quest_data as QD
from data import seeker_data as SKD

import time

def getQuestInfosFromCache(t):
    p = BigWorld.player()
    if p and hasattr(p, "questInfoCache") and t in p.questInfoCache:
        results = []
        for questId in p.questInfoCache[t]:
            results.append(QuestInfo(questId))
        return results
    return None

class QuestInfo:

    def __init__(self, questId):
        self.questId = questId
        self.questData = QD.data.get(questId, {})

    def canComplete(self):
        p = BigWorld.player()

        if not p:
            return false

        return commQuest.completeQuestCheck(p, self.questId, True)

    def getName(self):
        return self.questData.get("name", "")