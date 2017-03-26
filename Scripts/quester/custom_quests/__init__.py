import roplus

import os 
import imp
import sys

CUSTOM_QUEST_GOALS_COMPLETORS = {}

def reloadCustomQuestCompletors():
    global CUSTOM_QUEST_GOALS_COMPLETORS
    CUSTOM_QUEST_GOALS_COMPLETORS = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(dir_path):
        if file.endswith(".py") and not file.startswith("__"):
            filePath = os.path.join(dir_path, file)
            mod_name = file[:-3]
            if mod_name in sys.modules:
                del sys.modules[mod_name]
            try:
                mod = __import__(mod_name, globals(), locals(), [], -1)
                if mod and hasattr(mod, "QUEST_GOAL_COMPLETORS"):
                    for quest, goalCompletors in mod.QUEST_GOAL_COMPLETORS.items():
                        roplus.log("Found custom quest completor for quest : " + str(quest))
                        CUSTOM_QUEST_GOALS_COMPLETORS[quest] = goalCompletors
            except Exception as e:
                roplus.log("Unable to load file : " + str(e))