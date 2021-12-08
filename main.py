
# MUST import from top-level or it gets a different instance from GUI scripts
from Pokemon_Battle_Sim.Trainer import *
from Pokemon_Battle_Sim.pokemon import Pokemon
from Pokemon_Battle_Sim.moves.move import move_factory
from Pokemon_Battle_Sim.moves.attacks import Struggle
from Pokemon_Battle_Sim.pubsub import Subscriber
from Pokemon_Battle_Sim.enums import Screen
from Pokemon_Battle_Sim.Model import Model
from Pokemon_Battle_Sim import use_gui
from Pokemon_Battle_Sim.Printer import Printer
from Pokemon_Battle_Sim import demo
from Pokemon_Battle_Sim import BattleBackend

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
    move = move_factory('Explosion')
    pokemon.add_move(move)
    Model.opponent.add_to_team(pokemon)
    pokemon = Pokemon(150)
    move = move_factory('Psychic')
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


class GUIPrinter(Subscriber):
    """Prints any messages to the appropriate textbox"""

if __name__ == '__main__':
    printer = Printer
    if use_gui:
        # Initialize GUI
        from gui.root import Root, menus
        root = Root()
        # root.open_menu(menus.BATTLE)
        root.open_menu(menus.MAIN_MENU)
        root.mainloop()
    else:
        # Run in console
        #
        demo.demo1(make_player=True)
        #
        # input("Press enter to continue.")
        # demo.demo1(make_player=True)
        #
        # input("Press enter to continue.")
        # demo.demo2(make_player=True)
        battle = BattleBackend.Battle()
        while Model.player.has_pokemon() and Model.opponent.has_pokemon():
            battle.battle_round()
