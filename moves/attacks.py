from moves.move import *


class Attack(Move):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self):
        pass


class StatAlteringAttack(Attack):
    def __init__(self, name):
        super(StatAlteringAttack, self).__init__(name)
        move = db.select(f'SELECT chance, stat, stages FROM stat_altering_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__stat = move[1]
        self.__stages = move[2]

    def use_move(self):
        pass


class SetDamageAttack(Attack):
    def __init__(self, name):
        super(SetDamageAttack, self).__init__(name)

    def use_move(self):
        pass


class FlinchAttack(Attack):
    def __init__(self, name):
        super(FlinchAttack, self).__init__(name)
        move = db.select(f'SELECT chance FROM flinch_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]

    def use_move(self):
        pass


class RecoilAttack(Attack):
    def __init__(self, name):
        super(RecoilAttack, self).__init__(name)

    def use_move(self):
        pass


class RecoilOnMissAttack(Attack):
    def __init__(self, name):
        super(RecoilOnMissAttack, self).__init__(name)

    def use_move(self):
        pass


class StatusEffectAttack(Attack):
    def __init__(self, name):
        super(StatusEffectAttack, self).__init__(name)

    def use_move(self):
        pass


class ConfusingContinuousAttack(Attack):
    def __init__(self, name):
        super(ConfusingContinuousAttack, self).__init__(name)

    def use_move(self):
        pass


class HealingAttack(Attack):
    def __init__(self, name):
        super(HealingAttack, self).__init__(name)

    def use_move(self):
        pass


class ChargingAttack(Attack):
    def __init__(self, name):
        super(ChargingAttack, self).__init__(name)

    def use_move(self):
        pass


class MultiAttack(Attack):
    def __init__(self, name):
        super(MultiAttack, self).__init__(name)

    def use_move(self):
        pass


class TrapAttack(Attack):
    def __init__(self, name):
        super(TrapAttack, self).__init__(name)

    def use_move(self):
        pass


class ConfusingAttack(Attack):
    def __init__(self, name):
        super(ConfusingAttack, self).__init__(name)

    def use_move(self):
        pass


class CritAttack(Attack):
    def __init__(self, name):
        super(CritAttack, self).__init__(name)

    def use_move(self):
        pass


class VanishingAttack(Attack):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self):
        pass


class DreamEater(Attack):
    def __init__(self, name):
        super(DreamEater, self).__init__(name)

    def use_move(self):
        pass


class SelfDestruct(Attack):
    def __init__(self, name):
        super(SelfDestruct, self).__init__(name)

    def use_move(self):
        pass


class RechargeAttack(Attack):
    def __init__(self, name):
        super(RechargeAttack, self).__init__(name)

    def use_move(self):
        pass


class Struggle(Attack):
    def __init__(self, name):
        super(Struggle, self).__init__(name)

    def use_move(self):
        pass
