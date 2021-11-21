# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:30:21 2021

@author: Brian
"""

import tkinter as tk

import util
from Pokemon_Battle_Sim.database import database as db

class team_select(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        util.gridconfigure(self, rw=[1, 20, 5], cw=[1, 1, 1, 1])
        
        # Back button (top left)
        def command():
            try:
                self.master.open_menu("MAIN MENU")
            except AttributeError:
                print("Go back to main menu")
        back = util.Button(self, text="Main Menu", command=command)
        back['font'] = (util.font[0], 10) # Not sure why "font" kwarg doesn't seem to work
        back.grid(row=0, column=0, sticky='NSW')
        
        # Search bar (top right)
        search = tk.Label(self, text="Search (WIP)", font=('Arial', 20))
        search.grid(row=0, column=1, columnspan=3, sticky='NSE')
        
        # Pokemon list (center left)
        plist = self.pokemon_list(self, bg='yellow')
        plist.grid(row=1, column=0, columnspan=1, sticky='NSEW')
        
        # Pokemon detail (center right)
        pdetail = self.pokemon_detail(self, bg='red')
        pdetail.grid(row=1, column=1, columnspan=3, sticky='NSEW')
        
        # Current team (bottom)
        team = tk.Frame(self, bg='cyan')
        team.grid(row=2, column=0, columnspan=4, sticky='NSEW')
        
    class pokemon_list(tk.Listbox):
        """
        Source: https://www.pythontutorial.net/tkinter/tkinter-listbox/
        """
        def __init__(self, parent, *args, **kwargs):
            # frame = tk.Frame(parent, bg='red')
            # util.gridconfigure(frame)
            # Create the StringVar list that is displayed
            full_list = db.select("SELECT * FROM pokemon")
            namelist = tk.StringVar(value=[f"{x[0]}.{x[1]}" for x in full_list])
            font = (util.font[0], int(0.5*util.font[1]))
            super().__init__(parent, listvariable=namelist, selectmode=tk.SINGLE,
                             font=font, width=0,
                             *args, **kwargs)
            # self.pack(expand=True, fill=tk.BOTH)
            self.grid(row=0, column=0)
            
    class pokemon_detail(tk.Frame):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            
        
if __name__ == "__main__":
    root = util.default_window()
    util.gridconfigure(root)
    menu = team_select(root)
    menu.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()