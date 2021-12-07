# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 12:42:49 2021

@author: Brian

The main game window that persists until player exits the game
Adapted from https://www.pythontutorial.net/tkinter/tkinter-object-oriented-window/
"""

from enum import Enum

from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.gui.main_menu import main_menu as _main_menu
from Pokemon_Battle_Sim.gui.team_select import team_select as _team_select
from Pokemon_Battle_Sim.gui.battle import Battle

class menus(Enum):
    MAIN_MENU = "MAIN MENU"
    TEAM_SELECT = "TEAM SELECT"
    BATTLE = "BATTLE"

class Root(util.Default_Window):
    def __init__(self):
        super().__init__()
        util.gridconfigure(self)
        self.frames = {}
        
        self.protocol('WM_DELETE_WINDOW', self.onDestroy) # https://stackoverflow.com/a/3295463/14501840
        self.bind('<Key>', self.handle_key)
        
        # Default to Main Menu
        self.open_menu(menus.MAIN_MENU)
        
    def mainloop(self):
        """Replacement for the default mainloop so that I can pause it for debugging"""
        self.run = True # Will be set False by handle_key or onDestroy, so this isn't an infinite loop
        while self.run:
            self.update()
        
    def handle_key(self, event):
        """Allows pausing and unpausing"""
        char = event.char
        if char == 'p':
            self.run = False
            
    def resume(self):
        self.run = True
        self.mainloop()
            
    def onDestroy(self):
        self.run = False
        self.destroy()
        
    def open_menu(self, menu):
        """With menus stacked on top of each other, choose which one to show on top
        source: https://www.pythontutorial.net/tkinter/tkraise/
        
        If menu has not been created yet, create it
        
        Parameters
        ----------
        menu : menus Enum
            Which menu to show"""
        if not isinstance(menu, menus):
            menu = menus(menu)
        
        if menu in self.frames:
            self.frames[menu].tkraise()
        else:
            mapper = {menus.MAIN_MENU: _main_menu,
                      menus.TEAM_SELECT: _team_select,
                      menus.BATTLE: Battle}
            frame = mapper[menu](self)
            util.grid(frame)
            self.frames[menu] = frame
        
if __name__ == "__main__":
    root = Root()
    root.mainloop()