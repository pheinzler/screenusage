#!/usr/bin/python3

import tkinter as tk

class Main(tk.Frame):
    def __init__(self, master =None):
        tk.Frame.__init__(self, master)
        self.root = master      

        self.init()
        self.create_widgets()
    
    def init(self):
        self.root.minsize(400, 100) 
    
    def create_widgets(self):
        self.lable = tk.Label(self.root, text= "Start tracking mouse movement and clicking")
        self.lable.grid(row=0 , column= 0)
        self.start = tk.Button(self.root, text="Start", fg="green").grid(row=1, column=1)
        self.stop = tk.Button(self.root, text="Stop", fg="red").grid(row=1, column=2)
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Screenusage")
    main = Main(root)
    root.mainloop()