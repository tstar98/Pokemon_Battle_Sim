# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 14:51:18 2021

@author: Brian
"""

import tkinter as tk

import util

class main_menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='red') # Make it red so it's obvious where there's empty space
        
        util.gridconfigure(self, rw=[4, 1, 3]) # Title, Assemble Team, Reserved for future buttons
        
        # Title splash
        title_splash = self.title_splash(self)
        title_splash.grid(row=0, column=0, sticky='NSEW')
        
        # "Assemble Team" button
        def assemble_team():
            self.master.open_menu("TEAM SELECT")
        button = util.Button(self, text='Assemble Team', command=assemble_team)
        button.grid(row=1, column=0, sticky='NSEW')
        
        # TODO?
        # Other buttons (high scores?)
        reserved = tk.Frame(self, bg='grey')
        reserved.grid(row=2, column=0, sticky='NSEW')
    
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
    root = tk.Tk()
    mm = main_menu(root)
    mm.grid(row=0, column=0)
    root.mainloop()