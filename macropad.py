from macro import Macro
from keyboard import Keyboard
from actions import *
from macro_factory import *
from xmlparser import Element, InvalidDataException

import sys

import re

def setup():
    kb = Keyboard()

    if len(sys.argv) == 1:
        return [loadFile("example-macros-1.xml", kb), loadFile("example-macros-2.xml", kb)]

    targets = sys.argv[1:]
    layers = []
    for path in targets:
        layers.append(loadFile(path, kb))

    return layers

def loadFile(file_path: str, keyboard: Keyboard):
    factory = MacroFactory(keyboard)

    macros = []

    with open(file_path, "r") as macrospec:
        header = macrospec.readline().strip()
        if header != "<!DOCTYPE macrospec>":
            raise InvalidDataException("Missing '<!DOCTYPE macrospec>' header")
        
        data = macrospec.read().strip()
        data_clean = re.sub(r'[\n\t]', '', data)
        data_clean = re.sub(r'  +', '', data_clean)
        
        elements = []
        active_el = Element()

        for c in data_clean:
            active_el.push(c)
            if active_el.closed:
                elements.append(active_el)
                active_el = Element()

        for el in elements:
            # print(f"{el.tag}: {el.attributes['name']}")
            # for ch in el.children:
            #     print(f"\t{ch.tag} ({ch.body})")

            macros.append(factory.create(el))

        return macros

def main():
    layers = setup()

    active_layer = 0

    while True:
        cmd = input()

        if cmd == 'switch':
            active_layer = (active_layer+1)%len(layers)
            print(f'switched to layer {active_layer+1}')
        elif cmd == 'quit':
            return
        else:
            try:
                num = int(cmd)
                if num in range(len(layers[active_layer])):
                    layers[active_layer][num].execute()
            except ValueError as v:
                print('Not a valid command')

if __name__ == '__main__':
    main()