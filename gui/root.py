# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 12:42:49 2021

@author: Brian

The main game window that persists until player exits the game
Adapted from https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
"""

import tkinter as tk
from enum import Enum

import util
import battle
from main_menu import main_menu as _main_menu
from team_select import team_select as _team_select

class menus(Enum):
    MAIN_MENU = "MAIN MENU"
    TEAM_SELECT = "TEAM SELECT"

class root(tk.Tk):
    def __init__(self):
        super().__init__()
        util.gridconfigure(self)
        self.frames = {}
        self.create_frames()
        
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
        
    def create_frames(self):
        """Create the various frames that can be shown"""
        # Main menu
        main_menu = _main_menu(self)
        main_menu.grid(row=0, column=0, sticky='NSEW')
        self.frames[menus.MAIN_MENU] = main_menu
        
        # Team selection
        team_select = _team_select(self)
        team_select.grid(row=0, column=0, sticky='NSEW')
        self.frames[menus.TEAM_SELECT] = team_select
        
    def open_menu(self, menu):
        """With menus stacked on top of each other, choose which one to show on top
        source: https://www.pythontutorial.net/tkinter/tkraise/
        
        Parameters
        ----------
        menu : menus Enum
            Which menu to show"""
        if not isinstance(menu, menus):
            menu = menus(menu)
        self.frames[menu].tkraise()
        
        
if __name__ == "__main__":
    root = root()
    root.open_menu(menus.MAIN_MENU)
    root.mainloop()