from xmlparser import Element, InvalidDataException
from macro import *
from actions import *

class ActionAccumulator:
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    def as_list(self):
        return self.actions

class MacroFactory:
    def __init__(self, keyboard):
        self.keyboard = keyboard

    def get_child_actions(self, definition, accumulator):
        for child in definition.children:
            if child.tag == "Tap":
                accumulator.add(Tap(child.body))
            elif child.tag == "Down":
                accumulator.add(Down(child.body))
            elif child.tag == "Up":
                accumulator.add(Up(child.body))
            elif child.tag == "Wait":
                accumulator.add(Wait(float(child.attributes["delay"])))
            elif child.tag == "TypeString":
                accumulator.add(TypeString(child.body))
            elif child.tag == "Repeat":
                acc = ActionAccumulator()
                self.get_child_actions(child, acc)
                accumulator.add(Repeat(acc.as_list(), int(child.attributes["times"])))

        return accumulator

    def create(self, definition: Element):
        if definition.tag != "macro":
            raise InvalidDataException("Macro is not wrapped by a <macro> element")
        
        macro = Macro(self.keyboard, definition.attributes["name"])

        self.get_child_actions(definition, macro)

        return macro
        

