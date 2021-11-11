import random

from enums import Stat
from moves.move import *


class ScreenMove(Move):
    def __init__(self, name):
        super(ScreenMove, self).__init__(name)
        move = db.select(f'SELECT screen_type from screen_moves where name = \'{name}\';')[0]
        self.__screen_type = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class SwitchingMove(Move):
    def __init__(self, name):
        super(SwitchingMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class StatAlteringMove(Move):
    def __init__(self, name):
        super(StatAlteringMove, self).__init__(name)
        move = db.select(f'SELECT self, stat, stages FROM stat_altering_moves WHERE name = \'{name}\';')[0]
        self._self_target = move[0]
        self._stat = move[1]
        self._stages = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if not self._does_hit(pokemon1.accuracy, pokemon2.evasion):
            return

        pokemon = pokemon1 if self._self_target else pokemon2
        message = pokemon.name + "'s "

        # determine stat and set function obj to correct stat altering function
        if self._stat == Stat.ATTACK.value:
            message += "attack "
            change_stat = pokemon.change_atk
        elif self._stat == Stat.DEFENSE.value:
            message += "defense "
            change_stat = pokemon.change_def
        elif self._stat == Stat.SPECIAL.value:
            message += "special "
            change_stat = pokemon.change_spc
        elif self._stat == Stat.SPEED.value:
            message += "speed "
            change_stat = pokemon.change_spe
        elif self._stat == Stat.EVASION.value:
            message += "evade "
            change_stat = pokemon.change_eva
        else:
            message += "accuracy "
            change_stat = pokemon.change_acc

        if change_stat(self._stages):
            if self._stages > 1 or self._stages < -1:
                message += "greatly "
            if self._stages > 0:
                message += "rose."
            else:
                message += "fell."

        else:
            # pokemon's stat won't change, either too high or too low,
            message += "won't go any "
            if self._stages > 0:
                message += "higher."
            else:
                message += "lower."

        self.publish(message)


class StatusEffectMove(Move):
    def __init__(self, name):
        super(StatusEffectMove, self).__init__(name)
        move = db.select(f'SELECT status_effect FROM status_effect_moves WHERE name = \'{name}\';')[0]
        self.__status_effect = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class HealingMove(Move):
    def __init__(self, name):
        super(HealingMove, self).__init__(name)
        self.__percent = 50

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class ConfusingMove(Move):
    def __init__(self, name):
        super(ConfusingMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class RandomMove(Move):
    def __init__(self, name):
        super(RandomMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        moves = db.select('SELECT * FROM random;')
        move_name = random.choice(moves)
        move = move_factory(move_name[0])
        move.use_move(pokemon1, pokemon2, reflect, light_screen)

        pass


class MimicMove(Move):
    def __init__(self, name):
        super(MimicMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class Rest(Move):
    def __init__(self, name):
        super(Rest, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class Splash(Move):
    def __init__(self, name):
        super(Splash, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self._pp -= 1
        self.publish("But nothing happened.")


class Transform(Move):
    def __init__(self, name):
        super(Transform, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class MirrorMove(Move):
    def __init__(self, name):
        super(MirrorMove, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass
