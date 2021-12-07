# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 17:25:05 2021

@author: Brian

The Model part of MVC
"""

from enum import Enum

from Pokemon_Battle_Sim.pubsub import ChannelPublisher
from Pokemon_Battle_Sim import Trainer
from Pokemon_Battle_Sim.pokemon import Pokemon

class channels(Enum):
    SELECTED_POKEMON = "SELECTED_POKEMON"
    SELECTED_MOVE = "SELECTED_MOVE"
    PLAYER = "PLAYER"
    OPPONENT = "OPPONENT"
    
# Use Python convention to hide constructor
class __Model(ChannelPublisher):
    def __init__(self):
        super().__init__()
        for channel in channels:
            self.add_channel(channel)
        
        # For managing the two teams
        self.player = Trainer.Player()
        self.player.add_subscriber(self.get_channel(channels.PLAYER))
        self.opponent = Trainer.Opponent()
        self.opponent.add_subscriber(self.get_channel(channels.OPPONENT))
        
        # Initialize the channels appropriately
        self.publish(channels.SELECTED_POKEMON, Pokemon(None))
        self.publish(channels.PLAYER, self.player)
        self.publish(channels.OPPONENT, self.opponent)
        
        
    def set_sel_pokemon(self, pokemon):
        self._selected_pokemon = pokemon
        self.publish(channels.SELECTED_POKEMON, pokemon)
        
    @property
    def sel_pokemon(self):
        return self.get_last(channels.SELECTED_POKEMON)
        
    def set_sel_move(self, move):
        self._selected_move = move
        self.publish(channels.SELECTED_MOVE, move)
    
    @property
    def sel_move(self):
        return self.get_last(channels.SELECTED_MOVE)
    
    def add_sel_move(self):
        """Adds the selected move to the selected Pokemon and publishes the
        "new" Pokemon so that subscribers display the new move"""
        self._selected_pokemon.add_move(self._selected_move)
        self.publish(channels.SELECTED_POKEMON, self._selected_pokemon)
Model = __Model()