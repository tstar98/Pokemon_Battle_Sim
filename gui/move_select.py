# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:46:54 2021

@author: Brian
"""

import tkinter as tk
from tkinter import font as tkFont
import functools

def open_gui(frame, pokemon):
    """
    @param panel - the panel to put the menu in
    @param pokemon - player's Pokemon
    
    @returns move_use - the selected move
    """
    root = frame.winfo_toplevel()
    scale = 4
    
    # Separate the back button from the moves
    row_weights = [3, 7]
    for i, weight in enumerate(row_weights):
        frame.rowconfigure(i, weight=weight)
    frame.columnconfigure(0, weight=1)
    
    # Create a font
    # font = tkFont.Font(family='GothicE', size=7*scale)
    font = tkFont.Font(family='Arial', size=7*scale)
    
    # Back section
    backFrame = tk.Frame(frame)
    backFrame.grid(row=0, sticky='NSEW')
    backFrame.columnconfigure(0, weight=1)
    backFrame.rowconfigure(0, weight=1)
    def go_back():
        root.destroy() # FIXME root # TODO go back instead of just closing
    back = tk.Button(backFrame, text='Back', command=go_back,
                     relief='ridge', borderwidth=1*scale,
                     font=font)
    back.pack(fill=tk.BOTH, expand=True)
    
    # Moves section
    movesFrame = tk.Frame(frame, bg='grey',
                          relief='sunken', borderwidth=4*scale,
                          pady=1*scale)
    movesFrame.grid(row=1, sticky='NSEW')
    movesFrame.rowconfigure(0, weight=1)
    
    # Moves buttons
    move_use = [None]
    def select_move(move):
        move_use[0] = move
        root.destroy() # FIXME
    moves = pokemon.moves
    for col in range(len(moves)):
        movesFrame.columnconfigure(col, weight=1)
    for col, move in enumerate(moves):
        # Create the callback function with the move filled in
        callback = functools.partial(select_move, move)
        # Create the button, using the created callback
        button = tk.Button(movesFrame, text=move.name, command=callback,
                           relief='raised', borderwidth=1*scale,
                           font=font)
        button.grid(row=0, column=col, sticky='NSEW', padx=1*scale)
        
    # FIXME
    root.mainloop()
        
    return move_use[0]
    
if __name__ == "__main__":
    # Hacky code to mess with the path, since this script usually won't be run directly anyway
    # https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
    import sys, os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.split(SCRIPT_DIR)[0]
    if PARENT_DIR not in sys.path:
        sys.path.append(PARENT_DIR)
    if SCRIPT_DIR not in sys.path:
        sys.path.append(SCRIPT_DIR)
    from pokemon import Pokemon
    from moves.move import move_factory
    
    # FIXTURE: create the TKinter window
    window = tk.Tk()
    scale = 4
    res = [160*scale, 144*scale] # Original Game Boy Color resolution
    window.geometry(f"{res[0]}x{res[1]}")
    window.title('Pokemon Battle Simulator')
    # FIXTURE: create the TKinter frame
    frame = tk.Frame(window, bg='grey',
                     relief='sunken', borderwidth=4*scale,
                     pady=1*scale)
    frame.pack()
    
    # FIXTURE: create the pokemon
    pokemon = Pokemon(13)
    move = move_factory('Earthquake')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Rock Slide')
    pokemon.add_move(move)
    move = move_factory('Double Team')
    pokemon.add_move(move)
    del move
    
    move_use = open_gui(frame, pokemon)
    print(f"Selected {move_use.name}")