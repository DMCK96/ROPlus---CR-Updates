import roplus

import gametypes
import BigWorld

def cmpEnt(ent1, ent2):
    weight = {'Monster': 1,'Npc': 2,'QuestBox': 3,'Other': 4}
    clsName1 = ent1.__class__.__name__
    clsName2 = ent2.__class__.__name__
    w1 = weight.get(clsName1, 4)
    w2 = weight.get(clsName2, 4)
    if w1 != w2:
        return cmp(w1, w2)
    else:
        p = BigWorld.player()
        return cmp(ent1.position.distTo(p.position), ent2.position.distTo(p.position))

    return 0

def getEntities(maxRange=None):
    p = BigWorld.player()
    ents = [ ent for ent in BigWorld.entities.values() if not maxRange or ent.position.distTo(p.position) <= maxRange ]
    ents = sorted(ents, cmpEnt)
    return ents

def getAttackableEntities(maxRange=None):
    results = []
    p = BigWorld.player()
    ents = getEntities(maxRange)
    for ent in ents:
        if p.isEnemy(ent) and p.canBeTab(ent) and getattr(ent, 'life', gametypes.LIFE_DEAD) != gametypes.LIFE_DEAD and (hasattr(ent, 'canSelected') and ent.canSelected()):
            results.append(ent)
    return results

def findEntityByNpcId(npcId, maxRange=20):
    ents = getEntities(maxRange)
    for ent in ents:
        if getattr(ent, 'npcId', 0) == npcId:
            return ent
    return None

def findEntityByJiguanId(jiguanId, maxRange=20):
    ents = getEntities(maxRange)
    for ent in ents:
        if getattr(ent, 'jiguanId', 0) == jiguanId:
            return ent
    return None

def findEntityByCharType(charType, maxRange=20):
    ents = getEntities(maxRange)
    for ent in ents:
        if getattr(ent, 'charType', 0) == charType:
            return ent
    return None