#!/usr/bin/python3
from tkinter import Button
from pynput.mouse import Listener
import tkinter as tk


move_dic = dict()
move_dic["max"] = 0
move_dic["min"] = 0
click_dic = dict()
click_dic["max"] = 0
click_dic["min"] = 0

def on_move(x, y):
    dic_key = (int(x) , int(y))
    if dic_key in move_dic.keys():
        move_dic[dic_key] += 1
        if move_dic["max"] < move_dic[dic_key]:
            move_dic["max"] = move_dic[dic_key]
    else:
        move_dic[dic_key] = 1


def on_click(x, y, button, pressed):
    dic_key = (int(x) , int(y))
    if pressed:
        if dic_key in click_dic.keys():
            click_dic[dic_key] += 1
            if click_dic["max"] < click_dic[dic_key]:
                click_dic["max"] = click_dic[dic_key]
        else:
            click_dic[dic_key] = 1

def on_scroll(x, y, dx, dy):
    listener.stop()
    click_dic["min"] = click_dic["max"]
    move_dic["min"] = move_dic["max"]
    for ele in click_dic.values():
        if ele < click_dic["min"]:
            click_dic["min"] = ele
    
    for ele in move_dic.values():
        if ele < move_dic["min"]:
            move_dic["min"] = ele
    print("Move dict: \n" , move_dic, "\n\n")
    print("Click dict: \n" , click_dic)

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()