from actions import *

class Macro:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.sequence = []

    def add(self, action):
        self.sequence.append(action)
        
    def execute(self):
        for action in self.sequence:
            action.execute(self.keyboard)
