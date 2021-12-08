# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 14:51:18 2021

@author: Brian
"""

import functools
import tkinter as tk

from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim import demo
from Pokemon_Battle_Sim.Printer import ConsolePrinter
from Pokemon_Battle_Sim.Model import Model

class main_menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='red') # Make it red so it's obvious where there's empty space
        
        util.gridconfigure(self, rw=[4, 1, 1, 1, 1]) # Title, Assemble Team, Three Demos
        
        # Title splash
        title_splash = self.title_splash(self)
        title_splash.grid(row=0, column=0, sticky='NSEW')
        
        # "Assemble Team" button
        def assemble_team():
            try:
                self.master.open_menu("TEAM SELECT")
            except AttributeError:
                print("Go to team select")
        button = util.Button(self, text='Assemble Team', command=assemble_team)
        button.grid(row=1, column=0, sticky='NSEW')
        
        # "Demo Team" buttons
        def launch_demo(demo_func):
            demo_func(make_player=True)
            ConsolePrinter.update("Player team: " + ', '.join(p.name for p in Model.player.team()))
            ConsolePrinter.update("Opponent team: " + ', '.join(p.name for p in Model.opponent.team()))
            
            try:
                self.master.open_menu("BATTLE")
            except AttributeError:
                print("Start battle")
        for i in range(3):
            command = functools.partial(launch_demo, demo.demos[i])
            button = util.Button(self, text=f"Demo {i}", command=command)
            util.grid(button, row=i+2)
        
    def title_splash(self, parent):
        """Creates the title splash
        Used as a helper function when creating the main menu"""
        frame = tk.Frame(parent, bg='light grey')
        util.gridconfigure(frame, rw=[9, 3, 6, 1])
        
        # Title
        title = tk.Label(frame, bg='light grey', font=('Arial', 8*util.scale),
                         text="POKEMON BATTLE\nSIMULATOR")
        title.grid(row=0, column=0, sticky='NSEW')
        
        # Subtitle
        subtitle = tk.Label(frame, bg='light grey', font=('Arial', 4*util.scale),
                            text="Thomas Starnes & Brian Glassman")
        subtitle.grid(row=1, column=0, sticky='NSEW')
        subsubtitle = tk.Label(frame, bg='light grey', font=('Arial', 2*util.scale),
                               text="(No copyright infringement intended, please don't sue us Nintendo)")
        subsubtitle.grid(row=3, column=0, sticky='NSEW')
        
        return frame
    
if __name__ == "__main__":
    root = util.Default_Window()
    mm = main_menu(root)
    util.grid(mm)
    root.mainloop()