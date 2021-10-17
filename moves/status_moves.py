import random

from moves.move import *


class ScreenMove(Move):
    def __init__(self, name):
        super(ScreenMove, self).__init__(name)
        move = db.select(f'SELECT screen_type from screen_moves where name = \'{name}\';')[0]
        self.__screen_type = move[0]

    def use_move(self):
        pass


class SwitchingMove(Move):
    def __init__(self, name):
        super(SwitchingMove, self).__init__(name)

    def use_move(self):
        pass


class StatAlteringMove(Move):
    def __init__(self, name):
        super(StatAlteringMove, self).__init__(name)
        move = db.select(f'SELECT self, stat, stages FROM stat_altering_moves WHERE name = \'{name}\';')[0]
        self.__self_target = move[0]
        self.__stat = move[1]
        self.__stages = move[1]

    def use_move(self):
        pass


class StatusEffectMove(Move):
    def __init__(self, name):
        super(StatusEffectMove, self).__init__(name)
        move = db.select(f'SELECT status_effect FROM status_effect_moves WHERE name = \'{name}\';')[0]
        self.__status_effect = move[0]

    def use_move(self):
        pass


class HealingMove(Move):
    def __init__(self, name):
        super(HealingMove, self).__init__(name)
        self.__percent = 50

    def use_move(self):
        pass


class ConfusingMove(Move):
    def __init__(self, name):
        super(ConfusingMove, self).__init__(name)

    def use_move(self):
        pass


class RandomMove(Move):
    def __init__(self, name):
        super(RandomMove, self).__init__(name)

    def use_move(self):
        moves = db.select('SELECT * FROM random;')
        move_name = random.choice(moves)
        move = move_factory(move_name[0])
        move.use_move()

        pass


class MimicMove(Move):
    def __init__(self, name):
        super(MimicMove, self).__init__(name)

    def use_move(self):
        pass


class Rest(Move):
    def __init__(self, name):
        super(Rest, self).__init__(name)

    def use_move(self):
        pass


class Splash(Move):
    def __init__(self, name):
        super(Splash, self).__init__(name)

    def use_move(self):
        pass
