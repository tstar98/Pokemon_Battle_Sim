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
    pokemon = Pokemon(130)
    move = move_factory('Dragon Rage')
    pokemon.add_move(move)
    move = move_factory('Bite')
    pokemon.add_move(move)
    move = move_factory('Leer')
    pokemon.add_move(move)
    move = move_factory('Hydro Pump')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    pokemon = Pokemon(103)
    pokemon.add_move(move_factory("Toxic"))
    pokemon.add_move(move_factory("Mega Drain"))
    pokemon.add_move(move_factory("Psychic"))
    pokemon.add_move(move_factory("Rest"))
    Model.opponent.add_to_team(pokemon)

    pokemon = Pokemon(31)
    pokemon.add_move(move_factory("Double Kick"))
    pokemon.add_move(move_factory("Tail Whip"))
    pokemon.add_move(move_factory("Body Slam"))
    pokemon.add_move(move_factory("Poison Sting"))
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
    pokemon = Pokemon(130)
    move = move_factory('Dragon Rage')
    pokemon.add_move(move)
    move = move_factory('Bite')
    pokemon.add_move(move)
    move = move_factory('Leer')
    pokemon.add_move(move)
    move = move_factory('Hydro Pump')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    pokemon = Pokemon(103)
    pokemon.add_move(move_factory("Toxic"))
    pokemon.add_move(move_factory("Mega Drain"))
    pokemon.add_move(move_factory("Psychic"))
    pokemon.add_move(move_factory("Rest"))
    Model.opponent.add_to_team(pokemon)

    pokemon = Pokemon(31)
    pokemon.add_move(move_factory("Double Kick"))
    pokemon.add_move(move_factory("Tail Whip"))
    pokemon.add_move(move_factory("Body Slam"))
    pokemon.add_move(move_factory("Poison Sting"))
    Model.opponent.add_to_team(pokemon)

    if make_player:
        Model.player.team().clear()
        pokemon = Pokemon(143)
        move = move_factory('Rest')
        pokemon.add_move(move)
        move = move_factory('Headbutt')
        pokemon.add_move(move)
        move = move_factory('Amnesia')
        pokemon.add_move(move)
        move = move_factory('Hyper Beam')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)

        pokemon = Pokemon(150)
        move = move_factory('Psychic')
        pokemon.add_move(move)
        move = move_factory('Recover')
        pokemon.add_move(move)
        move = move_factory('Toxic')
        pokemon.add_move(move)
        move = move_factory('Ice Beam')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)

        pokemon = Pokemon(3)
        move = move_factory('Solar Beam')
        pokemon.add_move(move)
        move = move_factory('Poison Powder')
        pokemon.add_move(move)
        move = move_factory('Sleep Powder')
        pokemon.add_move(move)
        move = move_factory('Reflect')
        pokemon.add_move(move)
        Model.player.add_to_team(pokemon)


def demo2(make_player=True):
    Model.opponent.team().clear()
    pokemon = Pokemon(1)
    move = move_factory('Dragon Rage')
    pokemon.add_move(move)
    move = move_factory('Bite')
    pokemon.add_move(move)
    move = move_factory('Leer')
    pokemon.add_move(move)
    move = move_factory('Hydro Pump')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)
    #
    # pokemon = Pokemon(103)
    # pokemon.add_move(move_factory("Toxic"))
    # pokemon.add_move(move_factory("Mega Drain"))
    # pokemon.add_move(move_factory("Psychic"))
    # pokemon.add_move(move_factory("Rest"))
    # Model.opponent.add_to_team(pokemon)
    #
    # pokemon = Pokemon(31)
    # pokemon.add_move(move_factory("Double Kick"))
    # pokemon.add_move(move_factory("Tail Whip"))
    # pokemon.add_move(move_factory("Body Slam"))
    # pokemon.add_move(move_factory("Poison Sting"))
    # Model.opponent.add_to_team(pokemon)

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