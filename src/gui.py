#!/usr/bin/python3

import tkinter as tk

class Main(tk.Frame):
    def __init__(self, master =None):
        tk.Frame.__init__(self, master)
        self.root = master      

        self.init()
        self.create_widgets()
    
    def init(self):
        self.root.minsize(300, 100)
    
    def create_widgets(self):
        self.lable = tk.Label(self.root, text= "Start tracking mouse movement and clicking")
        self.lable.grid(row=0 , column= 0)
if __name__ == '__main__':
    root = tk.Tk()
    main = Main(root)
    root.mainloop()