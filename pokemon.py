import random
import math
from enum import Enum

from Pokemon_Battle_Sim.database import database as db
from Pokemon_Battle_Sim import enums
from Pokemon_Battle_Sim.moves.attacks import Confused
from Pokemon_Battle_Sim.pubsub import ChannelObservable
from Pokemon_Battle_Sim import MAX_MOVES
from Pokemon_Battle_Sim.Printer import Printer

class channels(Enum):
    PRINT = "PRINT"
    POKEMON = "POKEMON"

class Pokemon(ChannelObservable):
    def __init__(self, pokemon_id):
        # Initialize the Observable
        super().__init__()
        for channel in channels:
            self.add_channel(channel)
            
        # Initialize the Pokemon itself
        self.__level = 50
        self.__dv = 15
        self.__ev = 65535

        if pokemon_id is None:
            self.__id = None
            self.__name = ""
            self.__type1 = None
            self.__type2 = None
            self.__max_hp = None
            self.__hp = self.__max_hp
    
            self.__base_atk = 0
            self.__base_def = 0
            self.__base_spc = 0
            self.__base_spe = 0
        else:
            data = db.select(f'SELECT name, type1, type2, hp, attack, defense, special, speed FROM pokemon WHERE id = '
                             f'{pokemon_id};')[0]
    
            self.__id = pokemon_id
            self.__name = data[0]
            self.__type1 = data[1]
            self.__type2 = data[2]
            self.__max_hp = self.__determine_stat(data[3]) + self.__level + 10
            self.__hp = self.__max_hp
    
            self.__base_atk = data[4]
            self.__base_def = data[5]
            self.__base_spc = data[6]
            self.__base_spe = data[7]
        self.__attack = self.__determine_stat(self.__base_atk) + 5
        self.__defense = self.__determine_stat(self.__base_def) + 5
        self.__special = self.__determine_stat(self.__base_spc) + 5
        self.__speed = self.__determine_stat(self.__base_spe) + 5

        self.__moves = []
        self.__last_move = None
        self.__status_effect = enums.StatusEffect.NONE.value
        self.__sleep_counter = 0
        self.__poison_counter = 0
        self.__confused = False
        self.__confusion_counter = 0

        self.__battle_atk = 0
        self.__battle_def = 0
        self.__battle_spc = 0
        self.__battle_spe = 0
        self.__accuracy = 0
        self.__evasion = 0

        self.__flinch = False
        self.__trap_counter = 0
        self.__vanished = False

    def __determine_stat(self, base):
        a = (base + self.__dv) * 2
        b = math.ceil(math.sqrt(self.__ev))
        b = math.floor(b / 4)
        return math.floor(((a + b) * self.__level) / 100)

    def add_move(self, move):
        if len(self.__moves) >= MAX_MOVES:
            return False
        self.__moves.append(move)
        return True

    def reset_battle_stats(self):
        self.__battle_atk = 0
        self.__battle_def = 0
        self.__battle_spc = 0
        self.__battle_spe = 0
        self.__accuracy = 0
        self.__evasion = 0

    def can_move(self):
        """determines if pokemon is able to move, based on status_effect, flinch, confusion"""

        # pokemon can't move if opponent flinced them on same turn
        if self.__flinch:
            self.publish(f"{self.__name} flinched and can't attack.\n")
            return False

        if self.__status_effect == enums.StatusEffect.PARALYSIS.value:
            if 25 >= random.randint(1, 100):
                self.publish(f"{self.name} is paralyzed and is unable to attack.\n")
                return False

        # pokemon can't move if they are asleep
        # roll to wake up
        if self.__status_effect in (enums.StatusEffect.SLEEP.value, enums.StatusEffect.REST.value):
            # sleep turns only count if the pokemon is trying to use a move
            if self.__sleep_counter > 0:
                self.__sleep_counter -= 1
                self.publish(f"{self.name} is fast asleep.\n")
            else:
                self.publish(f"{self.name} woke up.\n")
                self.__status_effect = enums.StatusEffect.NONE.value
            return False

        # roll to see if damaged by confusion
        if self.__confused:
            # pokemon is no longer confused
            if self.__confusion_counter == 0:
                self.__confused = False
                self.publish(f"{self.__name} snapped out of confusion.")

            # pokemon is still confused
            else:
                self.publish(f"{self.name} is confused.")
                # confusion turns only count at this point
                self.__confusion_counter -= 1

                # pokemon takes damage and can't move
                if 50 >= random.randint(1, 100):
                    # cannot move due to confusion and hurts itself
                    Confused().use_move(self)
                    self.publish("It hurt itself in confusion.\n")
                    return False

        # pokemon can't move if they are trapped
        if self.__trap_counter > 0:
            self.publish(f"{self.__name} is trapped and cannot move.")
            return False

        return True

    def take_damage(self, damage):
        """ pokemon takes damage by given amount """
        self.__hp -= damage
        if self.__hp <= 0:
            self.__hp = 0
            self.publish(channels.PRINT, f'{self.__name} fainted.')
            self.publish(channels.POKEMON, "fainted")
        else:
            self.publish(channels.POKEMON, "health")

    def heal(self, health):
        """ heals pokemon by given amount """
        self.__hp += health
        if self.__hp > self.__max_hp:
            self.__hp = self.__max_hp
        self.publish(channels.POKEMON, "health")

    def next_turn(self):
        # take damage from status effects
        if self.__status_effect == enums.StatusEffect.BURN.value:
            self.take_damage(math.floor(self.__max_hp / 16))
            self.publish(f"{self.__name}'s hurt by the burn.\n")

        elif self.__status_effect == enums.StatusEffect.POISON.value:
            self.take_damage(math.floor(self.__max_hp / 16))
            self.publish(f"{self.__name}'s hurt by poison.\n")

        elif self.__status_effect == enums.StatusEffect.BAD_POISON.value:
            # if badly poisoned, pokemon takes N/16 of HP where N is 1-15
            self.take_damage(math.floor(self.__max_hp / 16) * self.__poison_counter)
            self.publish(f"{self.__name}'s hurt by poison.\n")
            self.__poison_counter = self.__poison_counter + 1 if self.__poison_counter < 15 else 15

        # take damage from trap
        if self.__trap_counter > 0:
            self.__trap_counter -= 1
            self.take_damage(math.floor(self.__max_hp / 16))
            self.publish(f"{self.__name}'s damaged by the trap.")

    def add_subscriber(self, arg1, arg2=None):
        if arg2 is None:
            channel = channels.PRINT
            subscriber = arg1
        else:
            channel = arg1
            subscriber = arg2
            
        super().add_subscriber(channel, subscriber)
            
        if channel == channels.PRINT:
            for move in self.__moves:
                move.add_subscriber(subscriber)

    def remove_subscriber(self, channel=None):
        raise NotImplementedError()
        # self.__sub = None
        # for move in self.__moves:
        #     move.remove_subscriber()

    def publish(self, arg1, arg2=None):
        if arg2 is None:
            channel = channels.PRINT
            message = arg1
        else:
            channel = arg1
            message = arg2
        super().publish(channel, message)

    def get_move(self, itr):
        if itr not in range(0, 3):
            return None
        return self.__moves[itr]

    def get_random_move(self):
        if len(self.__moves) == 0:
            return None
        return self.__moves[random.randint(0, len(self.__moves) - 1)]

    def has_moves(self):
        """returns False if all moves have 0 pp"""
        for move in self.__moves:
            if move.pp > 0:
                return True
        return False

    @property
    def pokemon_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def level(self):
        return self.__level

    @property
    def type1(self):
        return self.__type1

    @property
    def type2(self):
        return self.__type2

    @property
    def base_atk(self):
        return self.__base_atk

    @property
    def base_def(self):
        return self.__base_def

    @property
    def base_spc(self):
        return self.__base_spc

    @property
    def base_spe(self):
        return self.__base_spe

    @property
    def hp(self):
        return self.__hp

    @property
    def max_hp(self):
        return self.__max_hp

    @property
    def attack(self):
        return self.__attack

    @property
    def defense(self):
        return self.__defense

    @property
    def special(self):
        return self.__special

    @property
    def speed(self):
        return self.__speed

    @property
    def moves(self):
        return self.__moves

    @property
    def last_move(self):
        return self.__last_move

    @last_move.setter
    def last_move(self, move):
        self.__last_move = move

    @property
    def status_effect(self):
        return self.__status_effect

    @status_effect.setter
    def status_effect(self, stat_eff):
        """Sets pokemon's status effect to stat_eff given pokemon does not currently have a status effect
            or stat_eff is None or Rest"""
        if self.__status_effect == enums.StatusEffect.NONE.value\
                or stat_eff in (enums.StatusEffect.REST.value, enums.StatusEffect.NONE.value):
            self.__status_effect = stat_eff

            if stat_eff == enums.StatusEffect.NONE.value:
                return

            message = self.__name

            if stat_eff == enums.StatusEffect.SLEEP.value:
                message += ' fell asleep.'
                # pokemon will sleep for 1-7 turns
                self.__sleep_counter = random.randint(1, 7)

            if stat_eff == enums.StatusEffect.REST.value:
                message += ' started sleeping.'
                # pokemon will sleep for 2 turns
                self.__sleep_counter = 2

            if stat_eff == enums.StatusEffect.PARALYSIS.value:
                message += "'s paralyzed. It may not move."

            if stat_eff == enums.StatusEffect.BURN.value:
                message += "'s burned."

            if stat_eff == enums.StatusEffect.POISON.value:
                message += "'s poisoned."

            if stat_eff == enums.StatusEffect.BAD_POISON.value:
                message += "'s badly poisoned."
                self.__poison_counter = 1

            self.publish(message)

    @property
    def is_confused(self):
        return self.__confused

    @is_confused.setter
    def is_confused(self, boolean):
        if boolean:
            self.__confusion_counter = random.randint(2, 5)
            self.publish(f"{self.__name} became confused.")

        self.__confused = boolean

    def _stat_message(self, stage):
        if stage >= 2:
            return "greatly rose."
        if stage <= -2:
            return "greatly fell."
        if stage > 0:
            return "rose."
        if stage < 0:
            return "fell."

    def change_atk(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s attack won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s attack won't go any lower.")
            return False

        self.__battle_atk += stage
        self.publish(f"{self.name}'s attack {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__battle_atk > 6:
            self.__battle_atk = 6
        elif self.__battle_atk < -6:
            self.__battle_atk = -6

        return True

    def change_def(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s defense won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s defense won't go any lower.")
            return False

        self.__battle_def += stage
        self.publish(f"{self.name}'s defense {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__battle_def > 6:
            self.__battle_def = 6
        elif self.__battle_def < -6:
            self.__battle_def = -6

        return True

    def change_spc(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s special won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s special won't go any lower.")
            return False

        self.__battle_spc += stage
        self.publish(f"{self.name}'s special {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__battle_spc > 6:
            self.__battle_spc = 6
        elif self.__battle_spc < -6:
            self.__battle_spc = -6

        return True

    def change_spe(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s speed won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s speed won't go any lower.")
            return False

        self.__battle_spe += stage
        self.publish(f"{self.name}'s speed {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__battle_spe > 6:
            self.__battle_spe = 6
        elif self.__battle_spe < -6:
            self.__battle_spe = -6

        return True

    def change_acc(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s accuracy won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s accuracy won't go any lower.")
            return False

        self.__accuracy += stage
        self.publish(f"{self.name}'s accuracy {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__accuracy > 6:
            self.__accuracy = 6
        elif self.__accuracy < -6:
            self.__accuracy = -6

        return True

    def change_eva(self, stage):
        if stage > 0 and self.__evasion >= 6:
            self.publish(f"{self.__name}'s evasion won't go any higher.")
            return False
        if stage < 0 and self.__evasion <= -6:
            self.publish(f"{self.__name}'s evasion won't go any lower.")
            return False

        self.__evasion += stage
        self.publish(f"{self.__name}'s evasion {self._stat_message(stage)}")

        # ensure it is still between -6 and 6 after the update
        if self.__evasion > 6:
            self.__evasion = 6
        elif self.__evasion < -6:
            self.__evasion = -6

        return True

    @property
    def battle_atk(self):
        return self.__battle_stat(self.__battle_atk)

    @property
    def battle_def(self):
        return self.__battle_stat(self.__battle_def)

    @property
    def battle_spc(self):
        return self.__battle_stat(self.__battle_spc)

    @property
    def battle_spe(self):
        return self.__battle_stat(self.__battle_spe)

    @property
    def accuracy(self):
        # accuracy and evasion use a different formula, every stage raises / lowers by 1/3
        num = 3
        den = 3

        if self.__accuracy >= 0:
            num += self.__accuracy
        else:
            den += self.__accuracy

        return num / den

    @property
    def evasion(self):
        # accuracy and evasion use a different formula, every stage raises / lowers by 1/3
        num = 3
        den = 3

        if self.__evasion >= 0:
            num += self.__evasion
        else:
            den += self.__evasion

        return num / den

    def __battle_stat(self, stage):
        """ stage is the battle stat to be calculated as a floating point value
         increasing and decreasing a stat has diminishing returns """
        num = 2
        den = 2

        if stage >= 0:
            num += stage
        else:
            den -= stage

        return num / den

    @property
    def flinch(self):
        return self.__flinch

    @flinch.setter
    def flinch(self, boolean):
        self.__flinch = boolean

    @property
    def is_trapped(self):
        return True if self.__trap_counter > 0 else False

    @is_trapped.setter
    def is_trapped(self, boolean):
        # trapped for 2-5 turns
        num = random.randint(1, 200)
        if num <= 75:
            turns_trapped = 2
        elif num <= 150:
            turns_trapped = 3
        elif num <= 175:
            turns_trapped = 4
        else:
            turns_trapped = 5
        self.__trap_counter = turns_trapped

    @property
    def is_vanished(self):
        return self.__vanished

    @is_vanished.setter
    def is_vanished(self, boolean):
        self.__vanished = boolean

    def __str__(self):
        return f'Lv. {self.__level} {self.__name}\n{self.__hp} / {self.__max_hp}'
