# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 15:30:21 2021

@author: Brian
"""

import tkinter as tk

import util

class team_select(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        util.gridconfigure(self, [1, 20, 5], [1, 3])
        
        # Back button (top left)
        def command():
            try:
                self.master.open_menu("MAIN MENU")
            except AttributeError:
                print("Go back to main menu")
        back = util.Button(self, text="Main Menu", command=command)
        back.grid(row=0, column=0)
        
        # Search bar (top right)
        
        # Pokemon list (center)
        
        # Current team (bottom)
        
if __name__ == "__main__":
    root = tk.Tk()
    menu = team_select(root)
    menu.pack()
    root.mainloop()