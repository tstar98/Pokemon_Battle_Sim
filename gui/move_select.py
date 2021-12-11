# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:46:54 2021

@author: Brian

For choosing a move to use during battle
(Not for selecting moves during team select)
"""

import tkinter as tk
import functools
import itertools

from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.pubsub import Publisher, Observer
from Pokemon_Battle_Sim.Model import Model
from Pokemon_Battle_Sim.Trainer import channels as trainer_channels
from Pokemon_Battle_Sim import MAX_MOVES

class Move_Select(tk.Frame, Publisher, Observer):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        util.gridconfigure(self, rw=[3, 7])
        
        # Back section
        backFrame = tk.Frame(self)
        backFrame.grid(row=0, sticky='NSEW')
        util.gridconfigure(backFrame)
        back = util.Button(self, text='', command=None, state='disabled', disabledforeground="black")
        back.grid(row=0, column=0, sticky='NSEW')
        
        # Moves section
        movesFrame = tk.Frame(self, bg='grey',
                                   relief='sunken', borderwidth=4*util.scale,
                                   pady=1*util.scale)
        movesFrame.grid(row=1, column=0, sticky='NSEW')
        util.gridconfigure(movesFrame, cw=[1,1,1,1])
        
        # Moves buttons (empty for now, will be filled at first update)
        self.move_buttons = []
        for col in range(MAX_MOVES):
            button = util.Button(movesFrame)
            util.grid(button, column=col)
            self.move_buttons.append(button)
            
        # Initialize Publisher
        Publisher.__init__(self)
                
        # Initialize Observer
        Observer.__init__(self, Model.player, trainer_channels.TEAM)
        # Trigger update to fill the moves buttons
        self.update(None)
        
    def update(self, message):
        # Re-generate the moves buttons
        def select_move(move):
            Model.set_sel_move(move)
            self.publish(move)
        pokemon = self.subject.pokemon_out()
        for col, (move, button) in enumerate(itertools.zip_longest(pokemon.moves, self.move_buttons)):
            button = self.move_buttons[col]
            if move is None:
                button['text'] = ''
                button['command'] = None
            else:
                # Set the callback function with the move filled in
                button['text'] = move.name
                button['command'] = functools.partial(select_move, move)
        