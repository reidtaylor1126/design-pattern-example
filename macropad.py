from macro import Macro
from keyboard import Keyboard
from actions import *

def setup():
    kb = Keyboard()

    layer1 = [Macro(kb), Macro(kb), Macro(kb)]
    layer2 = [Macro(kb), Macro(kb), Macro(kb)]

    layer1[0].add(TypeString('Hello, world!'))

    layer1[1].add(Tap('f'))
    layer1[1].add(Tap('o'))
    layer1[1].add(Tap('o'))

    layer1[2].add(Repeat([TypeString('HAHA')], 5))

    layer2[0].add(TypeString('username'))
    layer2[0].add(Tap('tab'))
    layer2[0].add(TypeString('password'))
    layer2[0].add(Tap('return'))

    layer2[1].add(Tap('5'))
    layer2[1].add(Wait(1))
    layer2[1].add(Tap('4'))
    layer2[1].add(Wait(1))
    layer2[1].add(Tap('3'))
    layer2[1].add(Wait(1))
    layer2[1].add(Tap('2'))
    layer2[1].add(Wait(1))
    layer2[1].add(Tap('1'))
    layer2[1].add(Wait(1))
    layer2[1].add(TypeString('Blastoff!'))
    
    layer2[2].add(Down('win'))
    layer2[2].add(Down('x'))
    layer2[2].add(Up('x'))
    layer2[2].add(Up('win'))
    layer2[2].add(Wait(0.1))
    layer2[2].add(Tap('u'))
    layer2[2].add(Wait(0.1))
    layer2[2].add(Tap('s'))

    return layer1, layer2

def main():
    layers = setup()

    active_layer = 0

    while True:
        cmd = input()

        if cmd == 'switch':
            active_layer = (active_layer+1)%2
            print(f'switched to layer {active_layer+1}')
        elif cmd == 'quit':
            return
        else:
            try:
                num = int(cmd)
                if num in range(3):
                    layers[active_layer][num].execute()
            except ValueError as v:
                print('Not a valid number')

if __name__ == '__main__':
    main()