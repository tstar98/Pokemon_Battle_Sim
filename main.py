import random
from warnings import warn

from Trainer import *
from pokemon import Pokemon
from moves.move import move_factory
from moves.attacks import Struggle
from pubsub import Subscriber
from enums import Screen
# MUST import from top-level or it gets a different instance from GUI scripts
from Pokemon_Battle_Sim.Model import Model, channels
from Pokemon_Battle_Sim import use_gui

def select_team():
    """ player selects pokemon and moves """
    pass


def demo1():
    trainer1 = Model.opponent
    pokemon = Pokemon(51)
    move = move_factory('Earthquake')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Rock Slide')
    pokemon.add_move(move)
    move = move_factory('Double Team')
    pokemon.add_move(move)
    trainer1.add_to_team(pokemon)

    trainer2 = Model.player
    pokemon = Pokemon(28)
    move = move_factory('Fury Swipes')
    pokemon.add_move(move)
    move = move_factory('Swords Dance')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Take Down')
    pokemon.add_move(move)
    trainer2.add_to_team(pokemon)

    return trainer1, trainer2


def demo2():
    trainer1 = Model.opponent
    pokemon = Pokemon(65)
    move = move_factory('Thunder Wave')
    pokemon.add_move(move)
    move = move_factory('Confusion')
    pokemon.add_move(move)
    move = move_factory('Mega Punch')
    pokemon.add_move(move)
    move = move_factory('Recover')
    pokemon.add_move(move)
    trainer1.add_to_team(pokemon)

    trainer2 = Model.player
    pokemon = Pokemon(94)
    move = move_factory('Hypnosis')
    pokemon.add_move(move)
    move = move_factory('Dream Eater')
    pokemon.add_move(move)
    move = move_factory('Mimic')
    pokemon.add_move(move)
    move = move_factory('Confuse Ray')
    pokemon.add_move(move)
    trainer2.add_to_team(pokemon)

    return trainer1, trainer2


def demo3():
    trainer1 = Model.opponent
    pokemon = Pokemon(51)
    move = move_factory('Dragon Rage')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Rock Slide')
    pokemon.add_move(move)
    move = move_factory('Double Team')
    pokemon.add_move(move)
    trainer1.add_to_team(pokemon)

    trainer2 = Model.player
    pokemon = Pokemon(28)
    move = move_factory('Fury Swipes')
    pokemon.add_move(move)
    move = move_factory('Swords Dance')
    pokemon.add_move(move)
    move = move_factory('Rest')
    pokemon.add_move(move)
    move = move_factory('Take Down')
    pokemon.add_move(move)
    trainer2.add_to_team(pokemon)

    return trainer1, trainer2


def battle(trainer1, trainer2):
    """ where the battle occurs
     train1 is the player, train2 is the opponent"""

    while trainer1.has_pokemon() and trainer2.has_pokemon():
        make_selection(trainer1, trainer2)

        trainer1.next_turn()
        trainer1.pokemon_out().next_turn()

        trainer2.next_turn()
        trainer2.pokemon_out().next_turn()
        
        print(trainer1.pokemon_out())
        print()
        print(trainer2.pokemon_out())
        print()


def make_selection(trainer1, trainer2):
    # TODO: add checks for last move used

    move1 = trainer1.make_selection(trainer2.pokemon_out())
    move2 = trainer2.make_selection(trainer1.pokemon_out())

    # determine order of moves
    if move1.priority == move2.priority:
        if trainer1.pokemon_out().speed > trainer2.pokemon_out().speed:
            move_order = 1
        elif trainer1.pokemon_out().speed < trainer2.pokemon_out().speed:
            move_order = 2
        else:
            # randomly select order if priority and speed are the same
            move_order = random.randint(1, 2)

    elif move1.priority > move2.priority:
        move_order = 1
    else:
        move_order = 2

    if move_order == 1:
        use_moves(move1, trainer1, trainer2)
        # only use the move if both the attacker and target are still in battle
        if trainer1.pokemon_out().hp > 0 and trainer2.pokemon_out().hp > 0:
            use_moves(move2, trainer2, trainer1)

    else:
        use_moves(move2, trainer2, trainer1)
        # only use the move if both the attacker and target are still in battle
        if trainer1.pokemon_out().hp > 0 and trainer2.pokemon_out().hp > 0:
            use_moves(move1, trainer1, trainer2)


def use_moves(move, attacking_trainer, target_trainer):
    pokemon1 = attacking_trainer.pokemon_out()
    pokemon2 = target_trainer.pokemon_out()
    reflect = target_trainer.reflect
    light_screen = target_trainer.light_screen

    if not pokemon1.can_move():
        return

    # if all moves have 0 pp, struggle
    if True:
        warn("Pokemon.has_moves not implemented")
    else:
        if not pokemon1.has_moves:
            subscriber.update(f"{pokemon1.name} has no moves left.")
            subscriber.update(f"{pokemon1.name} used Struggle.")
            struggle = Struggle()
            struggle.use_move(pokemon1, pokemon2)
            return

    subscriber.update(f"{pokemon1.name} used {move.name}")
    result = move.use_move(pokemon1, pokemon2, reflect, light_screen)

    pokemon1.last_move = move

    # set up screens if the move did so
    if result is Screen.REFLECT:
        attacking_trainer.reflect = True
    elif result is Screen.LIGHT:
        attacking_trainer.light_screen = True


if __name__ == '__main__':
    subscriber = Subscriber()
    #
    # trainer1, trainer2 = demo1()
    # trainer1.add_subscriber(subscriber)
    # trainer2.add_subscriber(subscriber)
    # battle(trainer1, trainer2)
    #
    # input("Press enter to continue.")
    trainer1, trainer2 = demo2()
    trainer1.add_subscriber(subscriber)
    trainer2.add_subscriber(subscriber)
    battle(trainer1, trainer2)
    #
    # input("Press enter to continue.")
    # trainer1, trainer2 = demo3()
    # trainer1.add_subscriber(subscriber)
    # trainer2.add_subscriber(subscriber)
    
    if use_gui:
        # Initialize GUI
        from gui.root import Root, menus
