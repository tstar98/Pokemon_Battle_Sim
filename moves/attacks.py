from moves.move import *


class Attack(Move):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self):
        pass

    def crit(self):
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
        move = db.select(f'SELECT damage FROM set_damage_attacks WHERE name = \'{name}\';')[0]
        self.__damage = move[0]
        if self.__damage == 0:
            self.__use_move = self.half_damage
        elif self.__damage is None:
            self.__use_move = self.ohko
        else:
            self.__use_move = self.set_damage

    def use_move(self):
        self.__use_move()

    def set_damage(self):
        pass

    def half_damage(self):
        pass

    def ohko(self):
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
        move = db.select(f'SELECT recoil_percent FROM recoil_attacks WHERE name = \'{name}\';')[0]
        self.__recoil = move[0]

    def use_move(self):
        pass


class RecoilOnMissAttack(Attack):
    def __init__(self, name):
        super(RecoilOnMissAttack, self).__init__(name)
        self.__recoil = 1

    def use_move(self):
        pass


class StatusEffectAttack(Attack):
    def __init__(self, name):
        super(StatusEffectAttack, self).__init__(name)
        move = db.select(f'SELECT chance, status_effect FROM status_effect_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__status_effect = move[1]

    def use_move(self):
        pass


class ConfusingContinuousAttack(Attack):
    def __init__(self, name):
        super(ConfusingContinuousAttack, self).__init__(name)
        move = db.select(f'SELECT min_hits, max_hits FROM confusing_continuous_attacks WHERE name = \'{name}\';')[0]
        self.__counter = 0
        self.__min = move[0]
        self.__max = move[1]

    def use_move(self):
        pass


class HealingAttack(Attack):
    def __init__(self, name):
        super(HealingAttack, self).__init__(name)
        self.__percent = 50

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
        move = db.select(f'SELECT min_hits, max_hits FROM multi_attacks WHERE name = \'{name}\';')[0]
        self.__min = move[0]
        self.__max = move[1]

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
        move = db.select(f'SELECT chance FROM confusing_attacks WHERE name = \'{name}\'')[0]
        self.__chance = move[0]

    def use_move(self):
        pass


class CritAttack(Attack):
    def __init__(self, name):
        super(CritAttack, self).__init__(name)

    def use_move(self):
        super(CritAttack, self).use_move()
        pass

    def crit(self):
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
