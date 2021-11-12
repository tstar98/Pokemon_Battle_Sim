# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:46:54 2021

@author: Brian
"""

import tkinter as tk
from tkinter import font as tkFont
import functools

window = tk.Tk()
scale = 4
res = [160*scale, 144*scale] # Original Game Boy Color resolution
window.geometry(f"{res[0]}x{res[1]}")
window.title('Pokemon Battle Simulator')

# Create a base grid: main screen, back button, moves
row_weights = [12, 3, 7]
for i, weight in enumerate(row_weights):
    window.rowconfigure(i, weight=weight)
window.columnconfigure(0, weight=1)

# Create a font
font = tkFont.Font(family='GothicE', size=7*scale)

# Fight section
fight = tk.Frame(window, bg ='grey',
                 relief='sunken', borderwidth=4*scale, pady=1*scale)
fight.grid(row=0, sticky='NSEW')
fight.rowconfigure(0, weight=1)
fight.rowconfigure(1, weight=1)
fight.columnconfigure(0, weight=5)
fight.columnconfigure(1, weight=1)
fight.columnconfigure(2, weight=5)
them = tk.Frame(fight, bg='red',
                relief='raised', borderwidth=2*scale)
them.grid(row=0, column=1, columnspan=2, sticky="NSEW", padx=3*scale, pady=1*scale)
us = tk.Frame(fight, bg='green',
              relief='raised', borderwidth=2*scale)
us.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=3*scale, pady=1*scale)

# Back section
backFrame = tk.Frame(window)
backFrame.grid(row=1, sticky='NSEW')
backFrame.columnconfigure(0, weight=1)
backFrame.rowconfigure(0, weight=1)
def go_back():
    print("This would go back, but that's not implemented yet")
back = tk.Button(backFrame, text='Back', command=go_back,
                 relief='ridge', borderwidth=1*scale,
                 font=font)
back.pack(fill=tk.BOTH, expand=True)
# back.pack()

# Moves section
movesFrame = tk.Frame(window, bg='grey',
                      relief='sunken', borderwidth=4*scale,
                      pady=1*scale)
movesFrame.grid(row=2, sticky='NSEW')
movesFrame.rowconfigure(0, weight=1)
def use_move(move):
    print("Using " + move)
moves = ['Confuse Ray', 'Hydro Pump', 'Ice Beam', 'Body Slam']
for col in range(len(moves)):
    movesFrame.columnconfigure(col, weight=1)
for col, move in enumerate(moves):
    callback = functools.partial(use_move, move)
    button = tk.Button(movesFrame, text=move, command=callback,
                       relief='raised', borderwidth=1*scale,
                       font=font)
    button.grid(row=0, column=col, sticky='NSEW', padx=1*scale)

# Run the window
window.mainloop()
