# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:43:56 2021

@author: Brian
"""

import random

# MUST import from top-level or it gets a different instance from GUI scripts
import attacks
from Pokemon_Battle_Sim.moves.attacks import Struggle
from Pokemon_Battle_Sim.enums import Screen
from Pokemon_Battle_Sim.Model import Model
from Pokemon_Battle_Sim.Printer import ConsolePrinter, Printer


class Battle():
    """ where the battle occurs"""
    
    def battle_round(self):
        # check for last move used, certain classes of moves take multiple turns
        last_move = Model.player.pokemon_out().last_move
        if isinstance(last_move, attacks.ChargingAttack) and last_move.is_charged:
            player_move = last_move
        elif isinstance(last_move, attacks.RechargeAttack) and not last_move.is_charged:
            player_move = last_move
        elif isinstance(last_move, attacks.ConfusingContinuousAttack) and last_move.counter > 0:
            player_move = last_move
        else:
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

    def get_move(self, trainer):
        """checks for last move used and returns correct move selection"""
        # certain move classes take multiple turns
        last_move = trainer.pokemon_out().last_move
        if isinstance(last_move, attacks.ChargingAttack) and last_move.is_charged:
            return last_move
        elif isinstance(last_move, attacks.RechargeAttack) and not last_move.is_charged:
            return last_move
        elif isinstance(last_move, attacks.ConfusingContinuousAttack) and last_move.counter > 0:
            return last_move
        else:
            return Model.player.make_selection(Model.opponent.pokemon_out())

    def execute_moves(self, player_move, opponent_move):
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

        # Whether to switch Pokemon at the end of the round
        switch1 = False
        switch2 = False
        if Model.player.pokemon_out().hp == 0:
            switch1 = True
        if Model.opponent.pokemon_out().hp == 0:
            switch2 = True

        # player switches to next pokemon
        if switch1:
            self._switch(Model.player)

        # opponent switches to next pokemon
        if switch2:
            self._switch(Model.opponent)

        print()
        
    def _switch(self, trainer):
        """Convenience function to make Player/Opponent switch to next pokemon"""
        for pokemon in trainer.team():
            if pokemon == trainer.pokemon_out():
                continue
            if pokemon.hp > 0:
                trainer.switch_pokemon(pokemon)

    def use_moves(self, move, attacking_trainer, target_trainer):
        pokemon1 = attacking_trainer.pokemon_out()
        pokemon2 = target_trainer.pokemon_out()
        reflect = target_trainer.reflect
        light_screen = target_trainer.light_screen
    
        if not pokemon1.can_move():
            return
    
        # if all moves have 0 pp, struggle
        if not pokemon1.has_moves:
            Printer.update(f"{pokemon1.name} has no moves left.")
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
    
        # Switching out a pokemon needs the trainer. Work around for refactoring every subclass of Move
        elif callable(result):
            result(target_trainer)
