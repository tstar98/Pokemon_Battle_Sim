import random

from Pokemon_Battle_Sim.enums import Stat, StatusEffect, Screen
from Pokemon_Battle_Sim.moves.move import *


class ScreenMove(Move):
    def __init__(self, name):
        super(ScreenMove, self).__init__(name)
        move = db.select(f'SELECT screen_type from screen_moves where name = \'{name}\';')[0]
        self.__screen_type = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """ user sets up screen, returns screen enum key """
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if already set up
        if self.__screen_type == Screen.REFLECT.value and reflect != 0\
                or self.__screen_type == Screen.LIGHT.value and light_screen != 0:
            self.publish("But it failed.")
            return False

        return Screen.REFLECT if self.__screen_type == Screen.REFLECT.value else Screen.LIGHT

    @property
    def screen_type(self):
        return self.__screen_type


class SwitchingMove(Move):
    def __init__(self, name):
        super(SwitchingMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """returns function to switch Pokemon out that is to be called immediately"""
        self.publish(f"{pokemon1.name} used {self._name}.")
        return self._switch_pokemon

    def _switch_pokemon(self, trainer):
        switch_with = []

        # adds all of trainer's non-fainted Pokemon that are not in battle to list
        for pokemon in trainer.team():

            if pokemon is trainer.pokemon_out():
                continue
            if pokemon.hp > 0:
                switch_with.append(pokemon)

        if len(switch_with) == 0:
            self.publish("But it failed.")
            return False

        # select random pokemon
        pokemon = random.choice(switch_with)
        trainer.switch_pokemon(pokemon)


class StatAlteringMove(Move):
    def __init__(self, name):
        super(StatAlteringMove, self).__init__(name)
        move = db.select(f'SELECT self, stat, stages FROM stat_altering_moves WHERE name = \'{name}\';')[0]
        self._self_target = move[0]
        self._stat = move[1]
        self._stages = move[2]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        if not self._does_hit(pokemon1, pokemon2):
            return False

        pokemon = pokemon1 if self._self_target else pokemon2
        message = pokemon.name + "'s "

        # determine stat and set function obj to correct stat altering function
        if self._stat == Stat.ATTACK.value:
            change_stat = pokemon.change_atk
        elif self._stat == Stat.DEFENSE.value:
            change_stat = pokemon.change_def
        elif self._stat == Stat.SPECIAL.value:
            change_stat = pokemon.change_spc
        elif self._stat == Stat.SPEED.value:
            change_stat = pokemon.change_spe
        elif self._stat == Stat.EVASION.value:
            change_stat = pokemon.change_eva
        else:
            change_stat = pokemon.change_acc

        change_stat(self._stages)

        return True

    @property
    def stat(self):
        return self._stat


class StatusEffectMove(Move):
    def __init__(self, name):
        super(StatusEffectMove, self).__init__(name)
        move = db.select(f'SELECT status_effect FROM status_effect_moves WHERE name = \'{name}\';')[0]
        self.__status_effect = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if target already has a status effect
        if pokemon2.status_effect != StatusEffect.NONE.value:
            self.publish("But it failed.")
            return False

        # check accuracy
        if not self._does_hit(pokemon1, pokemon1):
            return False

        # check if it does not effect
        effectiveness = Move.get_effectiveness(self._type, pokemon2.type1) * Move.get_effectiveness(self._type, pokemon2.type2)
        if effectiveness == 0:
            self.publish(f"It doesn't affect {pokemon2.name}.")
            return False

        pokemon2.status_effect = self.__status_effect
        return True

    @property
    def status_effect(self):
        return self.__status_effect


class HealingMove(Move):
    def __init__(self, name):
        super(HealingMove, self).__init__(name)
        self._percent = 50

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if at full HP
        if pokemon1.hp == pokemon1.max_hp:
            self.publish("But it failed.")
            return False

        pokemon1.heal(math.ceil(pokemon1.max_hp * self._percent / 100))
        return True


class ConfusingMove(Move):
    def __init__(self, name):
        super(ConfusingMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if already confused
        if pokemon2.is_confused:
            self.publish("But it failed.")
            return False

        if not self._does_hit(pokemon1, pokemon2):
            return False

        pokemon2.is_confused = True


class RandomMove(Move):
    def __init__(self, name):
        super(RandomMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1
        moves = db.select('SELECT * FROM random;')
        move_name = random.choice(moves)
        move = move_factory(move_name[0])
        return move.use_move(pokemon1, pokemon2, reflect, light_screen)


class MimicMove(Move):
    """Copies a random move from opponent"""
    def __init__(self, name):
        super(MimicMove, self).__init__(name)
        self.__move = self

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        # if it has not been used, copy random move from opponent
        if self.__move is self:
            self.publish(f"{pokemon1.name} used {self._name}.")
            self._pp -= 1

            # copy random move
            if self._does_hit(pokemon1, pokemon2):
                move_selected = pokemon2.get_random_move()
                self.__move = move_factory(move_selected.name)
                self.__move.add_subscriber(Printer)
                self.publish(f"{pokemon1.name} learned {move_selected.name}.")

        # use copied move
        else:
            return self.__move.use_move(pokemon1, pokemon2, reflect, light_screen)

    # have to override property methods to get the copied move's properties
    @property
    def name(self):
        return self.__move._name

    @property
    def type(self):
        return self.__move._type

    @property
    def power(self):
        return self.__move._power

    @property
    def accuracy(self):
        return self.__move._accuracy

    @property
    def max_pp(self):
        return self.__move._max_pp

    @property
    def pp(self):
        return self.__move._pp

    @property
    def priority(self):
        return self.__move._priority

    @property
    def desc(self):
        return self.__move._desc

    def __str__(self):
        return f'{self.__move._name}\nPP = {self.__move._pp} / {self.__move._max_pp}'


class Rest(HealingMove):
    def __init__(self, name):
        super(Rest, self).__init__(name)
        self._percent = 100

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """ user falls asleep for 3 turns and regains full health """
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if pokemon has full health
        if pokemon1.hp == pokemon1.max_hp:
            self.publish("But it failed.")
            return False

        pokemon1.status_effect = StatusEffect.REST.value
        pokemon1.heal(pokemon1.max_hp)
        return True


class Splash(Move):
    def __init__(self, name):
        super(Splash, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1
        self.publish("But nothing happened.")
        return False


class Transform(Move):
    def __init__(self, name):
        super(Transform, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class MirrorMove(Move):
    def __init__(self, name):
        super(MirrorMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """Uses the opponent's last move"""
        self.publish(f"{pokemon1.name} used {self._name}.")
        self._pp -= 1

        # fails if last move is None or Mirror Move
        if pokemon2.last_move is None or isinstance(pokemon2.last_move.name, MirrorMove):
            self.publish("But it failed.")
            return False

        # copy opponent's last move and use it but discard the move afterwards
        move = move_factory(pokemon2.last_move.name)
        self.publish(f"{pokemon1} used {move.name}.")
        return move.use_move(pokemon1, pokemon2, reflect, light_screen)
