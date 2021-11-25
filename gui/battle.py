# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:16:03 2021

@author: Brian
"""

import tkinter as tk

from Pokemon_Battle_Sim.gui import move_select
from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim.pubsub import Subscriber

class Battle(tk.Frame): # The pokemon fighting and the move-select menu
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Create a base grid: main screen, info/buttons
        util.gridconfigure(self, rw=[12, 10])
        
        # Show the fighting Pokemon
        field = self.Battlefield(self, bg ='grey')
        field.grid(row=0, column=0, sticky='NSEW')
        
        # Show the move selection buttons
        msel = util.Button(self, text='msel')
        msel.grid(row=1, column=0, sticky='NSEW')
    
    class Battlefield(tk.Frame): # Just the pokemon fighting
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, relief='sunken', borderwidth=4*util.scale, pady=1*util.scale,
                             *args, **kwargs)
            
            # Place player and opponent Pokemon diagonally
            util.gridconfigure(self, rw=[1, 1], cw=[5, 1, 5])
            
            # Pokemon
            opponent = self.Pokemon_Detail(self, channels.PLAYER, bg='red')
            opponent.grid(row=0, column=2, sticky='NSEW')
            player = self.Pokemon_Detail(self, channels.OPPONENT, bg='green')
            player.grid(row=1, column=0, sticky='NSEW')
            
            # Move selection
            # movesFrame = tk.Frame(self, bg='grey',
            #                       relief='sunken', borderwidth=4*util.scale,
            #                       pady=1*util.scale)
            # movesFrame.grid(row=1, sticky='NSEW')
            # movesFrame.rowconfigure(0, weight=1)
            
            # use_move = move_select.open_gui(movesFrame, t_pokemon)
            
            # return use_move
        
        class Pokemon_Detail(tk.Frame, Subscriber):
            def __init__(self, parent, channel, *args, **kwargs):
                super().__init__(parent, relief='raised', borderwidth=2*util.scale,
                                  *args, **kwargs)
                # self.grid(row=0, column=1, columnspan=2, sticky="NSEW",
                #           padx=3*util.scale, pady=1*util.scale)
                
                if channel is None:
                    pokemon = Pokemon(None)
                else:
                    pokemon = Model.get_last(channel)
                
                # Setup grid:
                # Pokemon name          Team status icons
                # Pokemon types
                # [Spacer]
                # Health
                util.gridconfigure(self, rw=[1,1,1,1], cw=[3,1])
                # Pokemon name
                name = tk.Label(self, text=pokemon.name)
                name.grid(row=0, column=0, columnspan=1, sticky="NSEW")
                # Pokemon types
                # TODO
                # Health
                health = tk.Label(self, text=pokemon.hp)
                health.grid(row=3, column=0, columnspan=2, sticky="NSEW")
                
                # Initialize Subscriber
                Subscriber.__init__(self)
                if channel is not None:
                    Model.add_subscriber(channel, self)
                
            def update(self, pokemon):
                self.name['text'] = pokemon.name
                self.health['text'] = pokemon.hp
    
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
    Model.player.add_subscriber(Model.get_channel(channels.PLAYER))
    Model.opponent.add_to_team(o_pokemon)
    Model.opponent.add_subscriber(Model.get_channel(channels.OPPONENT))
    
    Model.player.publish(t_pokemon)
    Model.opponent.publish(o_pokemon)
    
    # FIXTURE: create the base Tkinter window
    root = util.default_window()
    util.gridconfigure(root)
    battle = Battle(root)
    battle.grid(row=0, column=0, sticky='NSEW')
    root.mainloop()
    # use_move = open_gui(t_pokemon, o_pokemon)
    # if use_move is None:
    #     print("In battle: no move selected")
    # else:
    #     print(f"In battle: selected {use_move.name}")