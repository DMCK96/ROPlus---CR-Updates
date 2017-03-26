import roplus

import json
import os

def defaultSettings():
    return { 
        "lastUsedCombat":  "",
        "lastUsedProfile": "",
        "combats": {
            "attackRange": 15,
        },
    }

def saveSettings(s, name):
    fileName = roplus.getWorkingDirectory() + "\\Settings\\" + name + ".json"
    file = open(fileName, "w")
    file.write(json.dumps(s, indent=4))
    file.close()

def loadSettings(name):
    try:
        fileName = roplus.getWorkingDirectory() + "\\Settings\\" + name + ".json"
        file = open(fileName, "r")
        result = json.loads(file.read())
        file.close()
        return result
    except Exception:
        return defaultSettings()