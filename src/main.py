#!/usr/bin/python3
import sys
from tkinter import Button
from pynput.mouse import Listener

def on_move(x, y):
    print ("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    print(type(x) , type(y))
    x_coord = int(x)
    print(x_coord)    
    if pressed:
        print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    print ('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

#Main
def main(args):
    
    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

if __name__ == '__main__':
    main(sys.argv[1:])