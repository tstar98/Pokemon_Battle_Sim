import random

from Trainer import *
from moves.move import move_factory
from pokemon import Pokemon
from pubsub import Subscriber


def select_team():
    """ player selects pokemon and moves """
    train = Player()
    pokemon = Pokemon(143)
    move = move_factory('Tackle')
    pokemon.add_move(move)
    train.add_to_team(pokemon)

    return train


def create_opponent():
    """ creates opponent trainer with random pokemon and moves """
    train = Opponent()
    pokemon = Pokemon(6)
    move = move_factory('Flamethrower')
    pokemon.add_move(move)
    move = move_factory("Leer")
    pokemon.add_move(move)
    train.add_to_team(pokemon)

    return train


def battle(train1, train2):
    """ where the battle occurs
     train1 is the player, train2 is the opponent"""

    print(train1.pokemon_out())
    print()
    print(train2.pokemon_out())
    print()

    while train1.has_pokemon() and train2.has_pokemon():

        move1 = train1.make_selection()
        move2 = train2.make_selection()

        # determine order of moves
        if move1.priority == move2.priority:
            if train1.pokemon_out().speed > train2.pokemon_out().speed:
                move_order = 1
            elif train1.pokemon_out().speed < train2.pokemon_out().speed:
                move_order = 2
            else:
                move_order = random.randint(1, 2)

        elif move1.priority > move2.priority:
            move_order = 1
        else:
            move_order = 2

        if move_order == 1:
            subscriber.update(f"{train1.pokemon_out().name} used {move1.name}")
            move1.use_move(train1.pokemon_out(), train2.pokemon_out())
            print()

            # pokemon can only use move if they are still in battle after the opponent used their move
            if train2.pokemon_out().hp > 0:
                subscriber.update(f"{train2.pokemon_out().name} used {move2.name}")
                move2.use_move(train2.pokemon_out(), train1.pokemon_out())
                print()

        else:
            subscriber.update(f"{train2.pokemon_out().name} used {move2.name}")
            move2.use_move(train2.pokemon_out(), train1.pokemon_out())
            print()

            # pokemon can only use move if they are still in battle after the opponent used their move
            if train1.pokemon_out().hp > 0:
                subscriber.update(f"{train1.pokemon_out().name} used {move1.name}")
                move1.use_move(train1.pokemon_out(), train2.pokemon_out())
                print()

        print(train1.pokemon_out())
        print()
        print(train2.pokemon_out())
        print()


if __name__ == '__main__':
    subscriber = Subscriber()

    trainer1 = select_team()
    trainer1.add_subscriber(subscriber)
    trainer2 = create_opponent()
    trainer2.add_subscriber(subscriber)

    battle(trainer1, trainer2)
