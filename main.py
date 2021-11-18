import random

from Trainer import *
from pokemon import Pokemon
from moves.move import move_factory
from pubsub import Subscriber


def select_team():
    """ player selects pokemon and moves """
    pass


def demo1():
    trainer1 = Opponent()
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

    trainer2 = Player()
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
    trainer1 = Opponent()
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

    trainer2 = Player()
    pokemon = Pokemon(94)
    move = move_factory('Hypnosis')
    pokemon.add_move(move)
    move = move_factory('Dream Eater')
    pokemon.add_move(move)
    # move = move_factory('Explosion')
    # pokemon.add_move(move)
    move = move_factory('Confuse Ray')
    pokemon.add_move(move)
    trainer2.add_to_team(pokemon)

    return trainer1, trainer2


def demo3():
    trainer1 = Opponent()
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

    trainer2 = Player()
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

    print(trainer1.pokemon_out())
    print()
    print(trainer2.pokemon_out())
    print()

    while trainer1.has_pokemon() and trainer2.has_pokemon():
        make_selection(trainer1, trainer2)

        trainer1.next_turn()
        trainer1.pokemon_out().next_turn()

        trainer2.next_turn()
        trainer2.pokemon_out().next_turn()

        # print(trainer1.pokemon_out())
        # print()
        # print(trainer2.pokemon_out())
        # print()


def make_selection(trainer1, trainer2):
    move1 = trainer1.make_selection()
    move2 = trainer2.make_selection()

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
        if trainer1.pokemon_out().can_move():
            subscriber.update(f"{trainer1.pokemon_out().name} used {move1.name}")
            move1.use_move(trainer1.pokemon_out(), trainer2.pokemon_out())
            print()

        # pokemon can only use move if they are still in battle after the opponent used their move
        if trainer2.pokemon_out().hp > 0 and trainer2.pokemon_out().can_move():
            subscriber.update(f"{trainer2.pokemon_out().name} used {move2.name}")
            move2.use_move(trainer2.pokemon_out(), trainer1.pokemon_out())
            print()

    else:
        if trainer2.pokemon_out().can_move():
            subscriber.update(f"{trainer2.pokemon_out().name} used {move2.name}")
            move2.use_move(trainer2.pokemon_out(), trainer1.pokemon_out())
            print()

        # pokemon can only use move if they are still in battle after the opponent used their move
        if trainer1.pokemon_out().hp > 0 and trainer1.pokemon_out().can_move():
            subscriber.update(f"{trainer1.pokemon_out().name} used {move1.name}")
            move1.use_move(trainer1.pokemon_out(), trainer2.pokemon_out())
            print()


if __name__ == '__main__':
    subscriber = Subscriber()

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

    # input("Press enter to continue.")
    # trainer1, trainer2 = demo3()
    # trainer1.add_subscriber(subscriber)
    # trainer2.add_subscriber(subscriber)
    # battle(trainer1, trainer2)
