import roplus

class Engine:

    def __init__(self):
        self.states         = list()
        self.currentState   = None

    def pulse(self):
        for state in self.states:
            if state.needToRun():
                if self.currentState != state:
                    if self.currentState != None:
                        self.currentState.onLeave()
                    state.onEnter()
                    self.currentState = state
                state.run()
                break
            

class State:

    def __init__(self):
        self.name = "Unamed"

    def needToRun(self):
        return False

    def run(self):
        return None

    def onEnter(self):
        return None

    def onLeave(self):
        return None