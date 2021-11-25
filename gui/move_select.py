# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:46:54 2021

@author: Brian
"""

import tkinter as tk
import functools

import util
from Pokemon_Battle_Sim.pubsub import Publisher
from Pokemon_Battle_Sim.Model import Model, channels

class Move_Select(tk.Frame, Publisher):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        util.gridconfigure(self, rw=[3, 7])
        
        # Back section
        backFrame = tk.Frame(self)
        backFrame.grid(row=0, sticky='NSEW')
        util.gridconfigure(backFrame)
        def go_back():
            print("Go back")
        back = util.Button(self, text='Back', command=go_back)
        back.grid(row=0, column=0, sticky='NSEW')
        
        # Moves section
        movesFrame = tk.Frame(self, bg='grey',
                              relief='sunken', borderwidth=4*util.scale,
                              pady=1*util.scale)
        movesFrame.grid(row=1, column=0, sticky='NSEW')
        util.gridconfigure(movesFrame, cw=[1,1,1,1])
        
        # Moves buttons
        def select_move(move):
            self.publish(move)
            go_back()
        moves = Model.player.pokemon_out().moves
        for col, move in enumerate(moves):
            # Create the callback function with the move filled in
            callback = functools.partial(select_move, move)
            # Create the button, using the created callback
            button = util.Button(movesFrame, text=move.name, command=callback)
            button.grid(row=0, column=col, sticky='NSEW')
            
        # Initialize Publisher
        Publisher.__init__(self)
    
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
    del move
    Model.player.add_to_team(pokemon)
    
    
    # FIXTURE: create the base Tkinter window
    root = util.Default_Window()
    util.gridconfigure(root)
    frame = Move_Select(root)
    frame.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()
