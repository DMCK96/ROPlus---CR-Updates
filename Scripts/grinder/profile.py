import roplus

import json
import os

def defaultProfile():
    return { 
        "name":                 "Unamed",
        "randomizeHotspots":    False,
        "hotspots":             [],
    }

def getProfiles():
    result = []
    profilesPattern = roplus.getWorkingDirectory() + "\\Profiles"
    for file in os.listdir(profilesPattern):
        if file.endswith(".grinder"):
            result.append(file[:-8])
    return result

def saveProfile(profile):
    fileName = roplus.getWorkingDirectory() + "\\Profiles\\" + profile["name"] + ".grinder"
    file = open(fileName, "w")
    file.write(json.dumps(profile, indent=4))
    file.close()

def loadProfile(name):
    fileName = roplus.getWorkingDirectory() + "\\Profiles\\" + name + ".grinder"
    file = open(fileName, "r")
    result = json.loads(file.read())
    file.close()
    return result