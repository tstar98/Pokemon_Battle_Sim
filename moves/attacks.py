import math
import random

from Pokemon_Battle_Sim.enums import Stat, StatusEffect
from Pokemon_Battle_Sim.moves.move import *


class Attack(Move):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        """ returns False if it misses, damage if it hits """
        self._pp -= 1

        # calculate accuracy
        if not self._does_hit(pokemon1, pokemon2):
            return False

        return self._do_damage(pokemon1, pokemon2, reflect, light_screen)

    def _do_damage(self, pokemon1, pokemon2, reflect, light_screen):
        effectiveness = self._get_effectiveness(pokemon2.type1) * self._get_effectiveness(pokemon2.type2)

        if effectiveness == 0:
            self.publish(f"It doesn't effect {pokemon2.name}.")
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

        # stab = Same Type Attack Bonus
        stab = 1.5 if self.is_stab(pokemon1) else 1

        # damage formula found here: https://bulbapedia.bulbagarden.net/wiki/Damage
        damage = math.ceil(((2 * level / 5 + 2) * self._power * a / d) / 50 + 2) * stab * effectiveness
        if screen:
            damage /= 2
        damage = math.ceil(damage * random.randint(85, 100) / 100)

        if effectiveness > 1:
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

    def is_stab(self, pokemon):
        if self._type == pokemon.type1:
            return True
        return False


class StatAlteringAttack(Attack):
    def __init__(self, name):
        super(StatAlteringAttack, self).__init__(name)
        move = db.select(f'SELECT chance, stat, stages FROM stat_altering_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__stat = move[1]
        self.__stages = move[2]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(StatAlteringAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if damage and self.__adds_effect():
            # find correct stat, don't change if it can't go any lower (-6)
            if self.__stat == Stat.ATTACK.value and pokemon2.change_atk(self.__stages):
                self.publish(f"{pokemon2.name}'s attack was lowered.")
            if self.__stat == Stat.DEFENSE.value and pokemon2.change_def(self.__stages):
                self.publish(f"{pokemon2.name}'s defense was lowered.")
            if self.__stat == Stat.SPECIAL.value and pokemon2.change_spc(self.__stages):
                self.publish(f"{pokemon2.name}'s special was lowered.")
            if self.__stat == Stat.SPEED.value and pokemon2.change_spe(self.__stages):
                self.publish(f"{pokemon2.name}'s speed was lowered.")

        return damage

    def __adds_effect(self):
        if self.__chance >= random.randint(1, 100):
            return True
        return False


class SetDamageAttack(Attack):
    def __init__(self, name):
        super(SetDamageAttack, self).__init__(name)
        move = db.select(f'SELECT damage FROM set_damage_attacks WHERE name = \'{name}\';')[0]
        self.__damage = move[0]
        if self.__damage == 0:
            self.__use_move = self.half_damage

        elif self.__damage is None:
            if self._name == "Psywave":
                self.__use_move = self.psywave
            else:
                self.__use_move = self.level_based

        else:
            self.__use_move = self.set_damage

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        return self.__use_move(pokemon1, pokemon2)

    def set_damage(self, pokemon1, pokemon2):
        """ move damages pokemon2 by a set integer """
        effectiveness = self._get_effectiveness(pokemon2.type1) * self._get_effectiveness(pokemon2.type2)
        if effectiveness == 0:
            self.publish(f"It doesn't effect {pokemon2.name}.")

        if not self._does_hit(pokemon1, pokemon2):
            return False

        pokemon2.take_damage(self.__damage)
        return self.__damage

    def half_damage(self, pokemon1, pokemon2):
        pass

    def level_based(self, pokemon1, pokemon2):
        pass

    def psywave(self, pokemon1, pokemon2):
        pass


class OHKO(Attack):
    def __init__(self, name):
        super(OHKO, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if pokemon1.speed < pokemon2.speed:
            self.publish("But it failed.")

        if not self._does_hit(pokemon1, pokemon2):
            return False

        if self._get_effectiveness(pokemon2.type1) == 0 or self._get_effectiveness(pokemon2.type2) == 0:
            self.publish(f"It doesn't effect {pokemon2.name}.")
            return False

        else:
            self.publish("It's a one-hit K.O.")

        damage = pokemon2.hp
        pokemon2.take_damage(damage)
        return damage


class FlinchAttack(Attack):
    def __init__(self, name):
        super(FlinchAttack, self).__init__(name)
        move = db.select(f'SELECT chance FROM flinch_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(FlinchAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if self.__adds_effect():
            pokemon2.flinch = True

        return damage

    def __adds_effect(self):
        if self.__chance >= random.randint(1, 100):
            return True
        return False


class RecoilAttack(Attack):
    def __init__(self, name):
        super(RecoilAttack, self).__init__(name)
        move = db.select(f'SELECT recoil_percent FROM recoil_attacks WHERE name = \'{name}\';')[0]
        self.__recoil = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(RecoilAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if damage:
            recoil = math.ceil(damage * 25 / 100)
            self.publish(f'{pokemon1.name} is damaged by recoil.')
            pokemon1.take_damage(recoil)

        return damage


class RecoilOnMissAttack(Attack):
    def __init__(self, name):
        super(RecoilOnMissAttack, self).__init__(name)
        self.__recoil = 1

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(RecoilOnMissAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        if not damage:
            self.publish(f"{pokemon1.name} kept going and crashed.")
            pokemon1.take_damage(1)


class StatusEffectAttack(Attack):
    def __init__(self, name):
        super(StatusEffectAttack, self).__init__(name)
        move = db.select(f'SELECT chance, status_effect FROM status_effect_attacks WHERE name = \'{name}\';')[0]
        self.__chance = move[0]
        self.__status_effect = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(StatusEffectAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if damage and self.__adds_effect():
            pass
            # TODO: status effect

        return damage

    def __adds_effect(self):
        if self.__chance >= random.randint(1, 100):
            return True
        return False


class ConfusingContinuousAttack(Attack):
    def __init__(self, name):
        super(ConfusingContinuousAttack, self).__init__(name)
        move = db.select(f'SELECT min_hits, max_hits FROM confusing_continuous_attacks WHERE name = \'{name}\';')[0]
        self.__counter = 0
        self.__min = move[0]
        self.__max = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        # set the counter
        if self.__counter == 0:
            self.__counter = random.randint(self.__min, self.__max)
            self._pp -= 1
        else:
            self.__counter -= 1

        damage = self._do_damage(pokemon1, pokemon2, reflect, light_screen)

        # user becomes confused if the end of the counter
        if counter == 0:
            pokemon1.is_confused = True

    @property
    def counter(self):
        return self.__counter


class HealingAttack(Attack):
    def __init__(self, name):
        super(HealingAttack, self).__init__(name)
        self.__percent = 50

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(HealingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        if damage:
            pokemon1.heal(math.ceil(damage / 4))

        return damage


class ChargingAttack(Attack):
    def __init__(self, name):
        super(ChargingAttack, self).__init__(name)
        self._is_charged = False

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if self._is_charged:
            self.publish(f"{pokemon1.name} unleashed its energy.")
            damage = super(ChargingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        else:
            self._pp -= 1
            damage = 0
            self.publish(f"{pokemon1.name} began charging power.")

        self._is_charged = not self._is_charged
        return damage

    @property
    def is_charged(self):
        return self._is_charged


class MultiAttack(Attack):
    def __init__(self, name):
        super(MultiAttack, self).__init__(name)
        move = db.select(f'SELECT min_hits, max_hits FROM multi_attacks WHERE name = \'{name}\';')[0]
        self.__min = move[0]
        self.__max = move[1]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        self._pp -= 1

        effectiveness = self._get_effectiveness(pokemon2.type1) * self._get_effectiveness(pokemon2.type2)
        if effectiveness == 0:
            self.publish(f"It doesn't effect {pokemon2.name}.")

        if not self._does_hit(pokemon1, pokemon2):
            return False

        times_hit = random.randint(self.__min, self.__max)
        damage = 0
        for _ in range(times_hit):
            damage += self._do_damage(pokemon1, pokemon2, reflect, light_screen)

        message = f"It hit {times_hit} time"
        message += "s." if times_hit > 1 else "."
        self.publish(message)

        return damage


class TrapAttack(Attack):
    def __init__(self, name):
        super(TrapAttack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(TrapAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if damage:
            pokemon2.is_trapped = True

        return damage


class ConfusingAttack(Attack):
    def __init__(self, name):
        super(ConfusingAttack, self).__init__(name)
        move = db.select(f'SELECT chance FROM confusing_attacks WHERE name = \'{name}\'')[0]
        self.__chance = move[0]

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        damage = super(ConfusingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)

        if damage and self.__adds_effect():
            pokemon2.is_confused = True

        return damage

    def __adds_effect(self):
        if self.__chance >= random.randint(1, 100):
            return True
        return False


class CritAttack(Attack):
    def __init__(self, name):
        super(CritAttack, self).__init__(name)

    def _is_crit(self, speed):
        # formula found here: https://bulbapedia.bulbagarden.net/wiki/Critical_hit#Generation_I
        threshold = min(math.floor(8 * speed / 2), 255)
        if threshold >= random.randint(1, 256):
            return True
        return False


class VanishingAttack(ChargingAttack):
    def __init__(self, name):
        super(Attack, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if not self._is_charged:
            self._pp -= 1
            if self._name == "Fly":
                message = f"{pokemon1.name} flew up high."
            else:
                message = f"{pokemon1} dug a hole."

            damage = True
            pokemon1.is_vanished = True

        else:
            damage = super(ChargingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
            pokemon1.is_vanished = False

        return damage


class DreamEater(HealingAttack):
    def __init__(self, name):
        super(DreamEater, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        # fails if target is not asleep
        if pokemon2.status_effect not in (StatusEffect.REST.value, StatusEffect.SLEEP.value):
            self._pp -= 1
            self.publish("But it failed.")
            return False
        
        return super(DreamEater, self).use_move(pokemon1, pokemon2, reflect, light_screen)


class SelfDestruct(Attack):
    def __init__(self, name):
        super(SelfDestruct, self).__init__(name)

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        # user faints and then does damage
        pokemon1.take_damage(pokemon1.max_hp)

        effectiveness = self._get_effectiveness(pokemon2.type1) * self._get_effectiveness(pokemon2.type1)
        if effectiveness == 0:
            self.publish(f"It doesn't affect {pokemon2.name}.")
            return False

        if not self._does_hit(pokemon1, pokemon2):
            return False

        # slightly different formula from normal attack
        a = pokemon1.attack * pokemon1.battle_atk
        d = pokemon2.defense * pokemon2.battle_def
        screen = True if reflect > 0 else False

        # in gen 1 critical hit damage is based on level
        level = pokemon1.level
        if self._is_crit(pokemon1.base_spe):
            self.publish("It's a critical hit.")
            level *= 2

        # stab = Same Type Attack Bonus
        stab = 1.5 if self.is_stab(pokemon1) else 1

        # damage formula found here: https://bulbapedia.bulbagarden.net/wiki/Damage
        damage = math.ceil(((2 * level / 5 + 2) * self._power * a / d) / 50 + 2) * stab * effectiveness
        if screen:
            damage /= 2
        damage = math.ceil(damage * random.randint(85, 100) / 100)

        if effectiveness > 1:
            self.publish(f"It's super effective.")
        elif effectiveness < 1 and effectiveness != 0:
            self.publish(f"It's not very effective.")

        pokemon2.take_damage(damage)
        return damage


class RechargeAttack(ChargingAttack):
    def __init__(self, name):
        super(RechargeAttack, self).__init__(name)
        self._is_charged = True

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        if self._is_charged:
            self.publish(f"{pokemon1.name} unleashed its energy.")
            damage = super(ChargingAttack, self).use_move(pokemon1, pokemon2, reflect, light_screen)
        else:
            damage = 0
            self.publish(f"{pokemon1.name} began charging power.")

        self._is_charged = not self._is_charged
        return damage


class Confused(Attack):
    """ For when a pokemon is confused, not the attack Confusion """
    def __init__(self):
        super().__init__("Confused")

    def use_move(self, pokemon1, pokemon2=None, reflect=0, light_screen=0):
        """ pokemon1 hurts itself in confusion, pokemon2, reflect, light_screen are not used here """
        a = pokemon1.attack * pokemon1.battle_atk
        d = pokemon1.defense * pokemon1.battle_def
        damage = math.ceil(((2 * pokemon1.level / 5 + 2) * self._power * a / d) / 50 + 2)

        pokemon1.take_damage(damage)


class Struggle(RecoilAttack):
    def __init__(self, name):
        super(Struggle, self).__init__(name)
        self._power = 50

    def use_move(self, pokemon1, pokemon2, reflect=0, light_screen=0):
        pass
