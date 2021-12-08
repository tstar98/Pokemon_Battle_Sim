# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:16:03 2021

@author: Brian
"""

import random
from warnings import warn
import tkinter as tk

from Pokemon_Battle_Sim.gui.move_select import Move_Select
from Pokemon_Battle_Sim.gui import util
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim.pubsub import Publisher, Subscriber, Observer
from Pokemon_Battle_Sim.pokemon import Pokemon, channels as poke_channels
from Pokemon_Battle_Sim.enums import Screen
from Pokemon_Battle_Sim.moves.attacks import Struggle
from Pokemon_Battle_Sim.Trainer import channels as trainer_channels
from Pokemon_Battle_Sim.Printer import ConsolePrinter

class Battle(tk.Frame, Publisher, Subscriber): # The pokemon fighting and the move-select menu
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
        
        # Initialize the Publisher
        Publisher.__init__(self)
        
        # Initialize the Subscriber
        Subscriber.__init__(self)
        msel.add_subscriber(self)
        
    def update(self, _):
        """Player selected a move, use it
        Note: could get the move from the message, but this way matches the
        method used for console battle"""
        self.battle_round()
        
    def battle_round(self):
        player_move = Model.player.make_selection(Model.opponent.pokemon_out())
        opponent_move = Model.opponent.make_selection(Model.player.pokemon_out())
        
        self.execute_moves(player_move, opponent_move)

        Model.player.next_turn()
        Model.player.pokemon_out().next_turn()

        Model.opponent.next_turn()
        Model.opponent.pokemon_out().next_turn()
        
        ConsolePrinter.update(Model.player.pokemon_out())
        ConsolePrinter.update()
        ConsolePrinter.update(Model.opponent.pokemon_out())
        ConsolePrinter.update()
                
    def gui_battle(self):
        while Model.player.has_pokemon() and Model.opponent.has_pokemon():
            self.battle_round()

    def execute_moves(self, player_move, opponent_move):
        # TODO: add checks for last move used
    
        # determine order of moves
        if player_move.priority == opponent_move.priority:
            if Model.player.pokemon_out().speed > Model.opponent.pokemon_out().speed:
                move_order = 1
            elif Model.player.pokemon_out().speed < Model.opponent.pokemon_out().speed:
                move_order = 2
            else:
                # randomly select order if priority and speed are the same
                move_order = random.randint(1, 2)
    
        elif player_move.priority > opponent_move.priority:
            move_order = 1
        else:
            move_order = 2
    
        if move_order == 1:
            self.use_moves(player_move, Model.player, Model.opponent)
            # only use the move if both the attacker and target are still in battle
            if Model.player.pokemon_out().hp > 0 and Model.opponent.pokemon_out().hp > 0:
                self.use_moves(opponent_move, Model.opponent, Model.player)
    
        else:
            self.use_moves(opponent_move, Model.opponent, Model.player)
            # only use the move if both the attacker and target are still in battle
            if Model.player.pokemon_out().hp > 0 and Model.opponent.pokemon_out().hp > 0:
                self.use_moves(player_move, Model.player, Model.opponent)
                
    def use_moves(self, move, attacking_trainer, target_trainer):
        pokemon1 = attacking_trainer.pokemon_out()
        pokemon2 = target_trainer.pokemon_out()
        reflect = target_trainer.reflect
        light_screen = target_trainer.light_screen
    
        if not pokemon1.can_move():
            return
    
        # if all moves have 0 pp, struggle
        if not pokemon1.has_moves:
            self.publish(f"{pokemon1.name} has no moves left.")
            struggle = Struggle()
            struggle.use_move(pokemon1, pokemon2)
            return
    
        result = move.use_move(pokemon1, pokemon2, reflect, light_screen)
    
        pokemon1.last_move = move
    
        # set up screens if the move did so
        if result is Screen.REFLECT:
            attacking_trainer.reflect = True
        elif result is Screen.LIGHT:
            attacking_trainer.light_screen = True

    
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