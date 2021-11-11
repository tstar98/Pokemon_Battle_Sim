import math
import random

from moves.move import *


super_effective = {
    "NORMAL": [],
    "FIRE": ["GRASS", "ICE", "BUG"],
    "WATER": ["FIRE", "GROUND", "ROCK"],
    "GRASS": ["WATER", "GROUND", "ROCK"],
    "ELECTRIC": ["WATER", "FLYING"],
    "ICE": ["GRASS", "GROUND", "FLYING", "DRAGON"],
    "FIGHTING": ["NORMAL", "ICE", "ROCK"],
    "POISON": ["GRASS", "BUG"],
    "GROUND": ["FIRE", "ELECTRIC", "POISON", "ROCK"],
    "FLYING": ["GRASS", "FIGHTING", "BUG"],
    "PSYCHIC": ["FIGHTING", "POISON"],
    "BUG": ["GRASS", "POISON", "PSYCHIC"],
    "ROCK": ["FIRE", "ICE", "FLYING", "BUG"],
    "GHOST": ["GHOST"],
    "DRAGON": ["DRAGON"]
}

not_very_effective = {
    "NORMAL": ["ROCK"],
    "FIRE": ["FIRE", "WATER", "ROCK", "DRAGON"],
    "WATER": ["WATER", "GRASS", "DRAGON"],
    "GRASS": ["FIRE", "GRASS", "POISON", "FLYING", "ROCK"],
    "ELECTRIC": ["GRASS", "ELECTRIC"],
    "ICE": ["WATER", "ICE"],
    "FIGHTING": ["POISON", "FLYING", "PSYCHIC"],
    "POISON": ["POISON", "GROUND", "GHOST"],
    "GROUND": ["GRASS", "BUG"],
    "FLYING": ["ELECTRIC", "ROCK"],
    "PSYCHIC": ["PSYCHIC"],
    "BUG": ["FIRE", "FIGHTING", "FLYING", "GHOST"],
    "ROCK": ["FIGHTING", "GROUND"],
    "GHOST": [],
    "DRAGON": []
}

no_effect = {
    "NORMAL": ["GHOST"],
    "FIRE": [],
    "WATER": [],
    "GRASS": [],
    "ELECTRIC": ['GROUND'],
    "ICE": [],
    "FIGHTING": ["GHOST"],
    "POISON": [],
    "GROUND": ["FLYING"],
    "FLYING": [],
    "PSYCHIC": [],
    "BUG": [],
    "ROCK": [],
    "GHOST": ["NORMAL", "PSYCHIC"],
    "DRAGON": []
}


class Attack(Move):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """ returns False if it misses, damage if it hits """
        self._pp -= 1

        # calculate accuracy
        if not self._does_hit(pokemon1.accuracy, pokemon2.evasion):
            self.publish('But it missed.')
            return False

        # determine category of move and whether a screen will play effect
        if self.category() == Category.PHYSICAL:
            a = pokemon1.attack * pokemon1.battle_atk
            d = pokemon2.defense * pokemon2.battle_def
            screen = True if reflect > 0 else False
        else:
            # in gen 1 special stat used for attack and defense of special moves
            a = pokemon1.special * pokemon1.battle_spc
            d = pokemon2.special * pokemon2.battle_spc
            screen = True if light_screen > 0 else False

        # in gen 1 critical hit damage is based on level
        level = pokemon1.level
        if self._is_crit(pokemon1.base_spe):
            self.publish("It's a critical hit.")
            level *= 2

        #
        stab = 1.5 if self.is_stab(pokemon1) else 1
        effectiveness = self.get_effectiveness(self._type, pokemon2.type1)
        if pokemon2.type2 is not None:
            effectiveness *= self.get_effectiveness(self._type, pokemon2.type2)

        # damage formula found here: https://bulbapedia.bulbagarden.net/wiki/Damage
        damage = math.ceil(((2 * level / 5 + 2) * self._power * a / d) / 50 + 2) * stab * effectiveness
        if screen:
            damage /= 2
        damage = math.ceil(damage * random.randint(85, 100) / 100)

        if effectiveness == 0:
            self.publish(f"It doesn't effect {pokemon2.name}.")
        elif effectiveness > 1:
            self.publish(f"It's super effective.")
        elif effectiveness < 1:
            self.publish(f"It's not very effective.")

        pokemon2.take_damage(damage)

        return damage

    def _is_crit(self, speed):
        # formula found here: https://bulbapedia.bulbagarden.net/wiki/Critical_hit#Generation_I
        threshold = math.floor(speed / 2)
        if threshold >= random.randint(1, 256):
            return True
        return False

    def _does_hit(self, accuracy, evasion):
        threshold = math.floor(self._accuracy * accuracy / evasion * 256)
        if threshold < random.randint(1, 256):
            return False
        return True

    def is_stab(self, pokemon):
        if self._type == pokemon.type1:
            return True
        return False

    def get_effectiveness(self, attack_type, defend_type):
        if defend_type in super_effective[attack_type]:
            return 2
        if defend_type in not_very_effective[attack_type]:
            return .5
        if defend_type in no_effect[attack_type]:
            return 0
        return 1


class StatAlteringAttack(Attack):
    def __init__(self, name):
        super(StatAlteringAttack, self).__init__(name)
        move = db.select(f'SELECT chance, stat, stages FROM stat_altering_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__stat = move[1]
        self.__stages = move[2]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        super(StatAlteringAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        # TODO: change stats


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

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        super(FlinchAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        # TODO: determine if opponent flinches


class RecoilAttack(Attack):
    def __init__(self, name):
        super(RecoilAttack, self).__init__(name)
        move = db.select(f'SELECT recoil_percent FROM recoil_attacks WHERE name = \'{name}\';')[0]
        self.__recoil = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(RecoilAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        recoil = math.ceil(damage * 25 / 100)
        self.publish(f'{pokemon1.name} is damaged by recoil.')
        pokemon1.take_damage(recoil)


class RecoilOnMissAttack(Attack):
    def __init__(self, name):
        super(RecoilOnMissAttack, self).__init__(name)
        self.__recoil = 1

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if not super(RecoilOnMissAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen):
            # TODO recoil
            pass


class StatusEffectAttack(Attack):
    def __init__(self, name):
        super(StatusEffectAttack, self).__init__(name)
        move = db.select(f'SELECT chance, status_effect FROM status_effect_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__status_effect = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        super(StatusEffectAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        # TODO: status effect


class ConfusingContinuousAttack(Attack):
    def __init__(self, name):
        super(ConfusingContinuousAttack, self).__init__(name)
        move = db.select(f'SELECT min_hits, max_hits FROM confusing_continuous_attacks WHERE name = \'{name}\';')[0]
        self.__counter = 0
        self.__min = move[0]
        self.__max = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class HealingAttack(Attack):
    def __init__(self, name):
        super(HealingAttack, self).__init__(name)
        self.__percent = 50

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(HealingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        if damage:
            pokemon1.heal(math.ceil(damage / 4))


class ChargingAttack(Attack):
    def __init__(self, name):
        super(ChargingAttack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class MultiAttack(Attack):
    def __init__(self, name):
        super(MultiAttack, self).__init__(name)
        move = db.select(f'SELECT min_hits, max_hits FROM multi_attacks WHERE name = \'{name}\';')[0]
        self.__min = move[0]
        self.__max = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class TrapAttack(Attack):
    def __init__(self, name):
        super(TrapAttack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class ConfusingAttack(Attack):
    def __init__(self, name):
        super(ConfusingAttack, self).__init__(name)
        move = db.select(f'SELECT chance FROM confusing_attacks WHERE name = \'{name}\'')[0]
        self.__chance = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class CritAttack(Attack):
    def __init__(self, name):
        super(CritAttack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass

    def crit(self):
        pass


class VanishingAttack(Attack):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class DreamEater(Attack):
    def __init__(self, name):
        super(DreamEater, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class SelfDestruct(Attack):
    def __init__(self, name):
        super(SelfDestruct, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class RechargeAttack(Attack):
    def __init__(self, name):
        super(RechargeAttack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass


class Struggle(Attack):
    def __init__(self, name):
        super(Struggle, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass
