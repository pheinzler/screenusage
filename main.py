#!/usr/bin/python3
from sys import argv
from pynput.mouse import Listener
from PIL import Image
import pickle

#create new data 
if len(argv) > 1:
    #load heatmap
    heatmap = Image.new('RGB', (3072, 1920), "white")
    move_dic = {"max":0}
    click_dic = {"max":0}

#use old data
else:
    heatmap = Image.open("heatmap.png")
    # loading Pickle Data sets
    with open("./data.pkl" , "rb") as data:
        data_arr = pickle.load(data)
        data.close() 
        #Store move and click coordinates in separate dictionaries
        move_dic = data_arr[0]
        click_dic = data_arr[1]

def create_image():
    for coordinate in move_dic.keys():
        if coordinate != "max" and coordinate != "min":
            heatmap.putpixel(coordinate , (255 , 255 , 0))
    for coordinate in click_dic.keys():
        if coordinate != "max" and coordinate != "min":
            heatmap.putpixel(coordinate , (255 , 0 , 0))

#mouse movement
def on_move(x, y):
    dic_key = (int(x) , int(y))
    if dic_key in move_dic.keys():
        move_dic[dic_key] += 1
        if move_dic["max"] < move_dic[dic_key]:
            move_dic["max"] = move_dic[dic_key]
    else:
        move_dic[dic_key] = 1
    
#clicking
def on_click(x, y, button, pressed):
    dic_key = (int(x) , int(y))
    if pressed:
        if dic_key in click_dic.keys():
            click_dic[dic_key] += 1
            if click_dic["max"] < click_dic[dic_key]:
                click_dic["max"] = click_dic[dic_key]
        else:
            click_dic[dic_key] = 1

#ending service rn
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

    #colourize pixels in image and safe data
    create_image()
    if len(argv) > 1:
    #store data
        with open("./data_new.pkl", "wb") as data:
            data_to_store = [move_dic , click_dic]
            pickle.dump(data_to_store , data)
            data.close()
            heatmap.save("heatmap_new.png")
            
    else:
        #store data
        with open("./data.pkl", "wb") as data:
            data_to_store = [move_dic , click_dic]
            pickle.dump(data_to_store , data)
            data.close()
            heatmap.save("heatmap.png")


with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
    
