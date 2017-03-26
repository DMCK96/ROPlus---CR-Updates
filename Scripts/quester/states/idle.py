import roplus

from roplus import fsm

class Idle(fsm.State):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.name = "Idle"

    def needToRun(self):
        return True

    def run(self):
        return

    def onEnter(self):
        return None

    def onLeave(self):
        return None
