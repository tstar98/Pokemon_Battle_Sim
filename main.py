import random

from Trainer import *
from moves.move import move_factory
from pokemon import Pokemon
from pubsub import Subscriber


def select_team():
    """ player selects pokemon and moves """
    trainer = Player()
    pokemon = Pokemon(26)
    move = move_factory('Thunder Wave')
    pokemon.add_move(move)
    trainer.add_to_team(pokemon)

    return trainer


def create_opponent():
    """ creates opponent trainer with random pokemon and moves """
    trainer = Opponent()
    pokemon = Pokemon(3)
    move = move_factory('Vine Whip')
    pokemon.add_move(move)
    trainer.add_to_team(pokemon)

    return trainer


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
                # randomly select order if priority and speed are the same
                move_order = random.randint(1, 2)

        elif move1.priority > move2.priority:
            move_order = 1
        else:
            move_order = 2

        if move_order == 1:
            if train1.pokemon_out().can_move():
                subscriber.update(f"{train1.pokemon_out().name} used {move1.name}")
                move1.use_move(train1.pokemon_out(), train2.pokemon_out())
                print()

            # pokemon can only use move if they are still in battle after the opponent used their move
            if train2.pokemon_out().hp > 0 and train2.pokemon_out().can_move():
                subscriber.update(f"{train2.pokemon_out().name} used {move2.name}")
                move2.use_move(train2.pokemon_out(), train1.pokemon_out())
                print()

        else:
            if train2.pokemon_out().can_move():
                subscriber.update(f"{train2.pokemon_out().name} used {move2.name}")
                move2.use_move(train2.pokemon_out(), train1.pokemon_out())
                print()

            # pokemon can only use move if they are still in battle after the opponent used their move
            if train1.pokemon_out().hp > 0 and train1.pokemon_out().can_move():
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
