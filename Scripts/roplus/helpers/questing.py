import BigWorld
import helpers.cellCmd
import commQuest
import const
from guis import uiUtils
from data import quest_data as QuestData
from data import seeker_data as SeekerData

class QuestGoal(object):
    def __new__(cls, goalItem):
        o = super(QuestGoal, cls).__new__(cls)
        o.description = goalItem.get(const.QUEST_GOAL_DESC, "")
        o.state = goalItem.get(const.QUEST_GOAL_STATE, False)
        o.track = goalItem.get(const.QUEST_GOAL_TRACK, False)
        o.trackSeekId = goalItem.get(const.QUEST_GOAL_TRACK_ID, 0)
        o.trackTaskType = goalItem.get(const.QUEST_GOAL_TRACK_TYPE, 0)
        o.type = goalItem.get(const.QUEST_GOAL_TYPE, True)
        o.order = goalItem.get(const.QUEST_GOAL_ORDER, "")
        o.trackSeekData = SeekerData.data.get(o.trackSeekId, {})
        return o