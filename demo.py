# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 18:22:25 2021

@author: Brian
"""

from Pokemon_Battle_Sim.pokemon import Pokemon
from Pokemon_Battle_Sim.moves.move import move_factory
from Pokemon_Battle_Sim.Model import Model

def demo0(make_player=True):
    Model.opponent.team().clear()
    pokemon = Pokemon(51)
    move = move_factory('Earthquake')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Rock Slide')
    pokemon.add_move(move)
    move = move_factory('Double Team')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    if make_player:
        Model.player.team().clear()
        pokemon = Pokemon(28)
        move = move_factory('Fury Swipes')
        pokemon.add_move(move)
        move = move_factory('Swords Dance')
        pokemon.add_move(move)
        move = move_factory('Rest')
        pokemon.add_move(move)
        move = move_factory('Take Down')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)


def demo1(make_player=True):
    Model.opponent.team().clear()
    pokemon = Pokemon(65)
    move = move_factory('Explosion')
    pokemon.add_move(move)
    # move = move_factory('Confusion')
    # pokemon.add_move(move)
    # move = move_factory('Mega Punch')
    # pokemon.add_move(move)
    # move = move_factory('Recover')
    # pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)
    pokemon = Pokemon(150)
    move = move_factory("Psychic")
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    if make_player:
        Model.player.team().clear()
        pokemon = Pokemon(94)
        move = move_factory('Hypnosis')
        pokemon.add_move(move)
        move = move_factory('Dream Eater')
        pokemon.add_move(move)
        move = move_factory('Mimic')
        pokemon.add_move(move)
        move = move_factory('Confuse Ray')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)


def demo2(make_player=True):
    Model.opponent.team().clear()
    pokemon = Pokemon(51)
    move = move_factory('Dragon Rage')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Rock Slide')
    pokemon.add_move(move)
    move = move_factory('Double Team')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    if make_player:
        Model.player.team().clear()
        pokemon = Pokemon(28)
        move = move_factory('Fury Swipes')
        pokemon.add_move(move)
        move = move_factory('Swords Dance')
        pokemon.add_move(move)
        move = move_factory('Rest')
        pokemon.add_move(move)
        move = move_factory('Take Down')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)
        
demos = [demo0, demo1, demo2]