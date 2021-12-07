import random
from warnings import warn

# MUST import from top-level or it gets a different instance from GUI scripts
from Pokemon_Battle_Sim.Trainer import *
from Pokemon_Battle_Sim.pokemon import Pokemon
from Pokemon_Battle_Sim.moves.move import move_factory
from Pokemon_Battle_Sim.moves.attacks import Struggle
from Pokemon_Battle_Sim.pubsub import Subscriber
from Pokemon_Battle_Sim.enums import Screen
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim import use_gui
from Pokemon_Battle_Sim.Printer import ConsolePrinter

def select_team():
    """ player selects pokemon and moves """
    pass


def demo1(make_player=True):
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


def demo2(make_player=True):
    pokemon = Pokemon(65)
    move = move_factory('Thunder Wave')
    pokemon.add_move(move)
    move = move_factory('Confusion')
    pokemon.add_move(move)
    move = move_factory('Mega Punch')
    pokemon.add_move(move)
    move = move_factory('Recover')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)

    if make_player:
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


def demo3(make_player=True):
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


class Battle(Subscriber):
    """ where the battle occurs"""
    
    def battle_round(self):
        self.make_selection()

        Model.player.next_turn()
        Model.player.pokemon_out().next_turn()

        Model.opponent.next_turn()
        Model.opponent.pokemon_out().next_turn()
        
        ConsolePrinter.update(Model.player.pokemon_out())
        ConsolePrinter.update()
        ConsolePrinter.update(Model.opponent.pokemon_out())
        ConsolePrinter.update()
            
    def console_battle(self):
        while Model.player.has_pokemon() and Model.opponent.has_pokemon():
            self.battle_round()

    def make_selection(self):
        # TODO: add checks for last move used
    
        move1 = Model.player.make_selection(Model.opponent.pokemon_out())
        move2 = Model.opponent.make_selection(Model.player.pokemon_out())
    
        # determine order of moves
        if move1.priority == move2.priority:
            if Model.player.pokemon_out().speed > Model.opponent.pokemon_out().speed:
                move_order = 1
            elif Model.player.pokemon_out().speed < Model.opponent.pokemon_out().speed:
                move_order = 2
            else:
                # randomly select order if priority and speed are the same
                move_order = random.randint(1, 2)
    
        elif move1.priority > move2.priority:
            move_order = 1
        else:
            move_order = 2
    
        if move_order == 1:
            use_moves(move1, Model.player, Model.opponent)
            # only use the move if both the attacker and target are still in battle
            if Model.player.pokemon_out().hp > 0 and Model.opponent.pokemon_out().hp > 0:
                use_moves(move2, Model.opponent, Model.player)
    
        else:
            use_moves(move2, Model.opponent, Model.player)
            # only use the move if both the attacker and target are still in battle
            if Model.player.pokemon_out().hp > 0 and Model.opponent.pokemon_out().hp > 0:
                use_moves(move1, Model.player, Model.opponent)

        print()


def use_moves(move, attacking_trainer, target_trainer):
    pokemon1 = attacking_trainer.pokemon_out()
    pokemon2 = target_trainer.pokemon_out()
    reflect = target_trainer.reflect
    light_screen = target_trainer.light_screen

    if not pokemon1.can_move():
        return

    # if all moves have 0 pp, struggle
    if not pokemon1.has_moves:
        subscriber.update(f"{pokemon1.name} has no moves left.")
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

class GUIPrinter(Subscriber):
    """Prints any messages to the appropriate textbox"""

if __name__ == '__main__':
    # make_player = not use_gui
    make_player = True
    
    #
    # demo1(make_player)
    #
    # input("Press enter to continue.")
    demo2(make_player)
    #
    # input("Press enter to continue.")
    # demo3(make_player)
    
    if use_gui:
        # Initialize GUI
        from gui.root import Root, menus
        root = Root()
        root.open_menu(menus.BATTLE)
        root.mainloop()
    else:
        # Run in console
        battle = Battle()
        battle.console_battle()
