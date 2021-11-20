# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 12:42:49 2021

@author: Brian

The main game window that persists until player exits the game
Adapted from https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
"""

import tkinter as tk

import util
import battle
from main_menu import main_menu as _main_menu

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        
        res = [160*util.scale, 144*util.scale] # Original Game Boy Color resolution
        self.geometry(f"{res[0]}x{res[1]}")
        self.title('Pokemon Battle Simulator')
        
        # Always open in screen center
        # https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (res[0]/2)
        y = (hs/2) - (res[1]/2)
        
        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (res[0], res[1], x, y))
        
    def open_battle(self, t_pokemon, o_pokemon):
        battle.open_gui(t_pokemon, o_pokemon)
        
if __name__ == "__main__":
    root = root()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_menu = _main_menu(root)
    main_menu.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()