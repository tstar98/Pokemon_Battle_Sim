# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:16:03 2021

@author: Brian
"""

import tkinter as tk

from Pokemon_Battle_Sim.gui.move_select import Move_Select
from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.Model import Model
from Pokemon_Battle_Sim.pubsub import Publisher, Subscriber, Observer
from Pokemon_Battle_Sim.pokemon import Pokemon, channels as poke_channels
from Pokemon_Battle_Sim.Trainer import channels as trainer_channels
from Pokemon_Battle_Sim.Printer import GUIPrinter

from Pokemon_Battle_Sim import BattleBackend

class Battle(tk.Frame, BattleBackend.Battle, Publisher, Subscriber): # The pokemon fighting and the move-select menu
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
        
        # Get ready for printing
        self.printout = self.Printout(self, row=1)
        GUIPrinter.add_subscriber(self.printout)
        
        
        # Initialize the Publisher
        Publisher.__init__(self)
        
        # Initialize the Subscriber
        Subscriber.__init__(self)
        msel.add_subscriber(self)
        
    def update(self, _):
        """Player selected a move, use it
        Note: could get the move from the message, but this way matches the
        method used for console battle"""
        battle_continuing = self.battle_round()
        if not battle_continuing:
            self.printout.update("GAME OVER")
        
    class Printout(Subscriber):
        def __init__(self, parent, *grid_args, **grid_kwargs):
            super().__init__()
            self.parent = parent
            self.grid_args = grid_args
            self.grid_kwargs = grid_kwargs
            
        def update(self, message):
            """Creates a button with the message so that it can be destroyed"""
            if message == "GAME OVER":
                player = Model.player.has_pokemon()
                opponent = Model.opponent.has_pokemon()
                if player and opponent:
                    raise RuntimeError("Ended early?")
                elif player and (not opponent):
                    text = "YOU WIN!!!"
                elif opponent and (not player):
                    text = "You lost :("
                elif (not player) and (not opponent):
                    text = "It's a draw..."
                tk_obj = tk.Label(self.parent, text=text,
                                    relief='ridge', borderwidth=1*util.scale)
                util.grid(tk_obj, *self.grid_args, **self.grid_kwargs)
            else:
                tk_obj = util.Button(self.parent, text=message)
                tk_obj['command'] = lambda: tk_obj.destroy()
                util.grid(tk_obj, *self.grid_args, **self.grid_kwargs)
    
    class Battlefield(tk.Frame): # Just the pokemon fighting
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent, relief='sunken', borderwidth=4*util.scale, pady=1*util.scale,
                             *args, **kwargs)
            
            # Place player and opponent Pokemon diagonally
            util.gridconfigure(self, rw=[1, 1], cw=[5, 1, 5])
            
            # Pokemon
            self.player = self.Team_Detail(self, Model.player, bg='green')
            self.player.grid(row=1, column=0, sticky='NSEW')
            self.opponent = self.Team_Detail(self, Model.opponent, bg='red')
            self.opponent.grid(row=0, column=2, sticky='NSEW')
            
        class Team_Detail(tk.Frame, Observer):
            """Frame to hold the Pokemon_Detail. Split off into a separate class
            because it needs to observe the team instead of the Pokemon"""
            def __init__(self, parent, team, *args, **kwargs):
                super().__init__(parent)
                util.gridconfigure(self)
                
                # Store args/kwargs for re-creating the detail later
                self.args = args
                self.kwargs = kwargs
                self.team = team
                self.create_detail()
                
                # Initialize Observer
                Observer.__init__(self, team, trainer_channels.TEAM)
                
            def create_detail(self):
                self.pokemon = self.Pokemon_Detail(self, self.team.pokemon_out(), *self.args, **self.kwargs)
                util.grid(self.pokemon)
                
            def update(self, message):
                """Team lineup changed, re-create the Pokemon_Detail"""
                self.create_detail()
        
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
                    Observer.__init__(self, pokemon, poke_channels.POKEMON)
                    
                def update(self, message=None):
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