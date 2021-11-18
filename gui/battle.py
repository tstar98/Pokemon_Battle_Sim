# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:16:03 2021

@author: Brian
"""

import tkinter as tk
from tkinter import font as tkFont

if __name__ == "__main__":
    import move_select
else:
    from gui import move_select

def open_gui(t_pokemon, o_pokemon):
    """
    

    Parameters
    ----------
    t_pokemon : Pokemon
        The player's Pokemon
    o_pokemon : Pokemon
        The opponent's Pokemon

    Returns
    -------
    None.

    """
    window = tk.Tk()
    scale = 4
    res = [160*scale, 144*scale] # Original Game Boy Color resolution
    window.geometry(f"{res[0]}x{res[1]}")
    window.title('Pokemon Battle Simulator')
    
    # Create a base grid: main screen, info/buttons
    row_weights = [12, 10]
    for i, weight in enumerate(row_weights):
        window.rowconfigure(i, weight=weight)
    window.columnconfigure(0, weight=1)
    
    # Fight section
    fight = tk.Frame(window, bg ='grey',
                     relief='sunken', borderwidth=4*scale, pady=1*scale)
    fight.grid(row=0, sticky='NSEW')
    fight.rowconfigure(0, weight=1)
    fight.rowconfigure(1, weight=1)
    fight.columnconfigure(0, weight=5)
    fight.columnconfigure(1, weight=1)
    fight.columnconfigure(2, weight=5)
    # Opponent
    them = tk.Frame(fight, bg='red',
                    relief='raised', borderwidth=2*scale)
    them.grid(row=0, column=1, columnspan=2, sticky="NSEW", padx=3*scale, pady=1*scale)
    # Trainer
    us = tk.Frame(fight, bg='green',
                  relief='raised', borderwidth=2*scale)
    us.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=3*scale, pady=1*scale)
    us.rowconfigure(0, weight=1) # Pokemon name ; Team status icons
    us.rowconfigure(1, weight=1) # Pokemon types
    us.rowconfigure(2, weight=1) # Blank spacer
    us.rowconfigure(3, weight=1) # Health
    us.columnconfigure(0, weight=3) # Left-aligned (most everything)
    us.columnconfigure(1, weight=1) # Right-aligned (team status icons)
    # Pokemon name
    name = tk.Label(us, text=t_pokemon.name)
    name.grid(row=0, column=0, columnspan=1, sticky="NSEW")
    # Pokemon types
    # TODO
    # Health
    health = tk.Label(us, text=t_pokemon.hp)
    health.grid(row=3, column=0, columnspan=2, sticky="NSEW")
    
    # Move selection
    movesFrame = tk.Frame(window, bg='grey',
                          relief='sunken', borderwidth=4*scale,
                          pady=1*scale)
    movesFrame.grid(row=2, sticky='NSEW')
    movesFrame.rowconfigure(0, weight=1)
    
    use_move = move_select.open_gui(movesFrame, t_pokemon)
    
    return use_move
    
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
    
    use_move = open_gui(pokemon, None)
    if use_move is None:
        print("In battle: no move selected")
    else:
        print(f"In battle: selected {use_move.name}")