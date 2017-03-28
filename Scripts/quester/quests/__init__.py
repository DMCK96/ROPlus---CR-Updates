import roplus

import os 
import imp
import sys

QUEST_COMPLETORS = {}

def reloadCustomQuestCompletors():
    global QUEST_COMPLETORS
    QUEST_COMPLETORS = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(dir_path):
        if file.endswith(".py") and not file.startswith("__"):
            filePath = os.path.join(dir_path, file)
            mod_name = file[:-3]
            if mod_name in sys.modules:
                del sys.modules[mod_name]
            try:
                mod = __import__(mod_name, globals(), locals(), [], -1)
                if mod and hasattr(mod, "QUEST_COMPLETORS"):
                    for questId, questCompletor in mod.QUEST_COMPLETORS.items():
                        roplus.log("Found custom quest completor for quest : " + str(questId))
                        QUEST_COMPLETORS[questId] = questCompletor
            except Exception as e:
                roplus.log("Unable to load file : " + str(e))
    roplus.log("Loaded " + str(len(QUEST_COMPLETORS)) + " custom quest completors")