import roplus

import os 
import imp

LOADED_COMBATS = {}

def reloadCombatModules():
    global LOADED_COMBATS
    LOADED_COMBATS = {}
    dir_path = roplus.getWorkingDirectory() + "\\Combats";
    for file in os.listdir(dir_path):
        if file.endswith(".py") and not file.startswith("__"):
            filePath = os.path.join(dir_path, file)
            mod_name = "Combats." + file
            try:
                combatmod = imp.load_source(mod_name, filePath)
                if combatmod and hasattr(combatmod, "Combat"):
                    try:
                        combat_inst = combatmod.Combat()
                        LOADED_COMBATS[combat_inst.name] = combat_inst
                        roplus.log("Combat script loaded : {0} ({1})".format(combat_inst.name, combat_inst.author))
                    except:
                        roplus.log("Unable to create Combat() class from file : " + file)
            except:
                roplus.log("Unable to load file : " + file)

class CombatBase(object):

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance.handleMove     = False
        instance.name           = "Unamed"
        instance.author         = "Author"
        return instance

    def onCombat(self, target):
        # Implement onCombat in your script
        return

reloadCombatModules()