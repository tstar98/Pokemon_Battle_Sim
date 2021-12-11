# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:46:54 2021

@author: Brian

For choosing a move to use during battle
(Not for selecting moves during team select)
"""

import tkinter as tk
import functools

from Pokemon_Battle_Sim.gui import util
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
        # TODO enable this when/if there are more options than fighting to the faint
        # def go_back():
        #     print("Go back")
        # back = util.Button(self, text='Back', command=go_back)
        def go_back():
            pass
        back = util.Button(self, text='', command=None, state='disabled', disabledforeground="black")
        back.grid(row=0, column=0, sticky='NSEW')
        
        # Moves section
        movesFrame = tk.Frame(self, bg='grey',
                              relief='sunken', borderwidth=4*util.scale,
                              pady=1*util.scale)
        movesFrame.grid(row=1, column=0, sticky='NSEW')
        util.gridconfigure(movesFrame, cw=[1,1,1,1])
        
        # Moves buttons
        def select_move(move):
            Model.set_sel_move(move)
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
        