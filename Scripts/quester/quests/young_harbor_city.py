import roplus
import quester
from roplus.helpers import nav
from roplus.helpers import entities
from quester.logics.quest_completor import GenericQuestCompletor

import const
import gameglobal
import BigWorld
from guis import uiConst
from helpers import qingGong

import time

class SharingDelicaciesCompletor(GenericQuestCompletor):

    def processQuestGoal(self, goal):
        p = BigWorld.player()
        if goal.order == "compItemCollect":
            itemToBuy = self.questData.get("compItemCollect", ())[0]
            sellerNpcId = goal.trackSeekData.get("npcId", 0)
            sellerNpc = entities.findEntityByNpcId(sellerNpcId, 100)
            if sellerNpc:
                self.skipQuestGoal = True
                self.skipAutoQuest = True
                if self.moveToEntity(sellerNpc, 3):
                    bagPage, bagPos = p.inv.searchBestInPages(itemToBuy, 1) # Search best slots in bag to put item
                    sellerNpc.cell.sell(0, 0, 1, bagPage, bagPos) # Buy item from page 0, slot 0
                    roplus.log("Buy item from " + sellerNpc.roleName)
                    self.bot.engine.wait(3)
        GenericQuestCompletor.processQuestGoal(self, goal)

# Tell the bot about the custom quest completor
QUEST_COMPLETORS = { 
    22120: SharingDelicaciesCompletor
}