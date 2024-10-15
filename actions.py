from abc import abstractmethod
from keyboard import Keyboard
import time

class KbAction:
    @abstractmethod
    def execute(self, keyboard: Keyboard):
        return
    
class Tap(KbAction):
    def __init__(self, key):
        self.key = key

    def execute(self, keyboard: Keyboard):
        keyboard.setkey(self.key, True)
        keyboard.setkey(self.key, False)
        return

class Down(KbAction):
    def __init__(self, key):
        self.key = key

    def execute(self, keyboard: Keyboard):
        keyboard.setkey(self.key, True)
        return

class Up(KbAction):
    def __init__(self, key):
        self.key = key

    def execute(self, keyboard: Keyboard):
        keyboard.setkey(self.key, False)
        return

class Wait(KbAction):
    def __init__(self, time):
        self.time = time

    def execute(self, keyboard: Keyboard):
        time.sleep(self.time)
        return
    
class TypeString(KbAction):
    def __init__(self, string):
        self.string = string

    def execute(self, keyboard: Keyboard):
        for ch in self.string:
            keyboard.setkey(ch, True)
            keyboard.setkey(ch, False)

class Repeat(KbAction):
    def __init__(self, sequence: list, times: int):
        self.sequence = sequence
        self.times = times

    def execute(self, keyboard: Keyboard):
        for _ in range(self.times):
            for action in self.sequence:
                action.execute(keyboard)
