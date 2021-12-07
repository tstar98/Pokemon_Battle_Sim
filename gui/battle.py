# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:16:03 2021

@author: Brian
"""

import tkinter as tk

from Pokemon_Battle_Sim.gui.move_select import Move_Select
from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim.pubsub import Subscriber, Observer
from Pokemon_Battle_Sim.pokemon import Pokemon

class Battle(tk.Frame): # The pokemon fighting and the move-select menu
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create a base grid: main screen, info/buttons
        util.gridconfigure(self, rw=[12, 10])
        
        # Show the fighting Pokemon
        self.field = self.Battlefield(self, bg ='grey')
        self.field.grid(row=0, column=0, sticky='NSEW')
        
        # Show the move selection buttons
        msel = Move_Select(self)
        msel.grid(row=1, column=0, sticky='NSEW')
    
    class Battlefield(tk.Frame): # Just the pokemon fighting
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, relief='sunken', borderwidth=4*util.scale, pady=1*util.scale,
                             *args, **kwargs)
            
            # Place player and opponent Pokemon diagonally
            util.gridconfigure(self, rw=[1, 1], cw=[5, 1, 5])
            
            # Pokemon
            if Model.player.has_pokemon():
                self.player = self.Pokemon_Detail(self, Model.player.pokemon_out(), bg='green')
            else:
                print("Player has no Pokemon to battle with")
                self.player = self.Pokemon_Detail(self, Pokemon(None), bg='green')
            self.player.grid(row=1, column=0, sticky='NSEW')
            if Model.opponent.has_pokemon():
                self.opponent = self.Pokemon_Detail(self, Model.opponent.pokemon_out(), bg='red')
            else:
                print("Opponent has no Pokemon to battle with")
                self.opponent = self.Pokemon_Detail(self, Pokemon(None), bg='red')
            self.opponent.grid(row=0, column=2, sticky='NSEW')
        
        class Pokemon_Detail(tk.Frame, Observer):
            def __init__(self, parent, pokemon, *args, **kwargs):
                super().__init__(parent, relief='raised', borderwidth=2*util.scale,
                                  *args, **kwargs)
                # self.grid(row=0, column=1, columnspan=2, sticky="NSEW",
                #           padx=3*util.scale, pady=1*util.scale)
                
                # Setup grid:
                #  -----------------------------------------
                # | Pokemon name          Team status icons |
                # | Pokemon types                           |
                # | [Spacer]                                |
                # | Health                                  |
                #  -----------------------------------------
                util.gridconfigure(self, rw=[1,1,1,1], cw=[3,1])
                # Pokemon name
                self.name = tk.Label(self, text=pokemon.name, bg=self["background"])
                self.name.grid(row=0, column=0, columnspan=1, sticky="NSEW")
                # Pokemon types
                # TODO
                # Health
                self.health = tk.Label(self, text=pokemon.hp, bg=self["background"])
                self.health.grid(row=3, column=0, columnspan=2, sticky="NSEW")
                
                # Initialize Observer
                Observer.__init__(self, pokemon)
                
            def update(self):
                self.name['text'] = self.subject.name
                self.health['text'] = self.subject.hp
                
    
if __name__ == "__main__":
    from Pokemon_Battle_Sim.pokemon import Pokemon
    from Pokemon_Battle_Sim.moves.move import move_factory
    
    # FIXTURE: create the pokemon
    if True:
        t_pokemon = Pokemon(13)
        move = move_factory('Earthquake')
        t_pokemon.add_move(move)
        move = move_factory('Rest')
        t_pokemon.add_move(move)
        move = move_factory('Rock Slide')
        t_pokemon.add_move(move)
        move = move_factory('Double Team')
        t_pokemon.add_move(move)
    
    # FIXTURE: create the pokemon
    if True:
        o_pokemon = Pokemon(42)
        move = move_factory('Earthquake')
        o_pokemon.add_move(move)
        move = move_factory('Rest')
        o_pokemon.add_move(move)
        move = move_factory('Rock Slide')
        o_pokemon.add_move(move)
        move = move_factory('Double Team')
        o_pokemon.add_move(move)
        
    # FIXTURE: setup the model
    Model.player.add_to_team(t_pokemon)
    Model.opponent.add_to_team(o_pokemon)
    
    # FIXTURE: create the base Tkinter window
    root = util.Default_Window()
    util.gridconfigure(root)
    battle = Battle(root)
    battle.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()
    # use_move = open_gui(t_pokemon, o_pokemon)
    # if use_move is None:
    #     print("In battle: no move selected")
    # else:
    #     print(f"In battle: selected {use_move.name}")