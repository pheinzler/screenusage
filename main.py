#!/usr/bin/python3
from sys import argv
from pynput.mouse import Listener
from PIL import Image
import pickle

#Constants
WIDTH = 3072
HEIGHT = 1920

# Colours
DARKBLUE = (0 , 0 , 153)
BRIGHTBLUE = (0 , 204 , 204)
YELLOW = (255 , 255 , 44)
BRIGHTORANGE = (249 , 191 , 30)
DARKORANGE = (239 , 134 , 13)
RED = (255,0,0)
DARKRED = (146 , 1 , 1)
GREEN = (94 , 225 , 133)
colours = [DARKBLUE, BRIGHTBLUE, GREEN, YELLOW, BRIGHTORANGE, DARKORANGE, RED, DARKRED]

#create new data 
if len(argv) > 1:
    #create heatmap
    heatmap_move = Image.new('RGB', (WIDTH, HEIGHT), "white")
    heatmap_click = Image.new('RGB', (WIDTH, HEIGHT), "white")
    move_dic = {"max":0}
    click_dic = {"max":0}

#use old data
else:
    heatmap_move = Image.open("heatmap_move.png")
    heatmap_click = Image.open("heatmap_click.png")
    # loading Pickle Data sets
    with open("./data.pkl" , "rb") as data:
        data_arr = pickle.load(data)
        data.close() 
        #Store move and click coordinates in separate dictionaries
        move_dic = data_arr[0]
        click_dic = data_arr[1]

def get_colour(coordinate, difference, dic):
    colour = None
    if dic == "move":
        val = move_dic[coordinate]
        min = move_dic["min"]
    elif dic == "click":
        val = click_dic[coordinate]
        min = click_dic["min"]
    one_part = difference / len(colours)
    for i in range (len(colours)):
        if i * one_part + min >= val:
            colour = colours[i]
            break
    if colour is None:
        colour = colours[len(colours) - 1]
    return colour
#colourize not just one pixel but square with more pixels
def colourize_more_pixels(x , y , colour , square = 5, image = None):
    if image == "move":
        if(x > WIDTH - square or y > HEIGHT - square):
            heatmap_move.putpixel((x,y) , colour)
        else:
            for i in range(x , x + square):
                for j in range(y , y + square):
                    heatmap_move.putpixel((i,j) , colour)
    elif image == "click":
        if(x > WIDTH - square or y > HEIGHT - square):
            heatmap_click.putpixel((x,y) , colour)
        else:
            for i in range(x , x + square):
                for j in range(y , y + square):
                    heatmap_click.putpixel((i,j) , colour)

def create_images():
    #get max and min values as well as differences for colour of pixel
    click_max , click_min , move_max , move_min = click_dic["max"] , click_dic["min"] , move_dic["max"] , move_dic["min"]
    move_difference = move_max - move_min
    click_difference = click_max - click_min
    for coordinate in move_dic.keys():
        if coordinate != "max" and coordinate != "min":
            colour = get_colour(coordinate , move_difference, "move")
            x = coordinate[0]
            y = coordinate[1]
            colourize_more_pixels(x,y, colour, image="move")
    for coordinate in click_dic.keys():
        if coordinate != "max" and coordinate != "min":
            colour = get_colour(coordinate , click_difference, "click")
            x = coordinate[0]
            y = coordinate[1]
            colourize_more_pixels(x,y, colour, image="click")

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
    #get min values
    click_dic["min"] = click_dic["max"]
    move_dic["min"] = move_dic["max"]
    for ele in click_dic.values():
        if ele < click_dic["min"]:
            click_dic["min"] = ele    
    for ele in move_dic.values():
        if ele < move_dic["min"]:
            move_dic["min"] = ele
    print("Creating Images...")
    #colourize pixels in image and safe data
    create_images()
    print("Images created")
    print("Store data")
    if len(argv) > 1:
        #store data
        with open("./data_new.pkl", "wb") as data:
            data_to_store = [move_dic , click_dic]
            pickle.dump(data_to_store , data)
            data.close()
            heatmap_click.save("heatmap_click_new.png")
            heatmap_move.save("heatmap_move_new.png")          
    else:
        #store data
        with open("./data.pkl", "wb") as data:
            data_to_store = [move_dic , click_dic]
            pickle.dump(data_to_store , data)
            data.close()
            heatmap_click.save("heatmap_click.png")
            heatmap_move.save("heatmap_move.png")
    print("Data stored")
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()