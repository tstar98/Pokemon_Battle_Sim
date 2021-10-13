from moves.move import *


class ScreenMove(Move):
    def __init__(self, name):
        super(ScreenMove, self).__init__(name)

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

    def use_move(self):
        pass


class StatusEffectMove(Move):
    def __init__(self, name):
        super(StatusEffectMove, self).__init__(name)

    def use_move(self):
        pass


class HealingMove(Move):
    def __init__(self, name):
        super(HealingMove, self).__init__(name)

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
        super(Splash, self).use_move()
        print('But nothing happened.')
