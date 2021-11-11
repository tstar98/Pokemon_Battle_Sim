import database.database as db
import math
import enums
from pubsub import Publisher


class Pokemon(Publisher):
    def __init__(self, pokemon_id):
        self.__level = 50
        self.__dv = 15
        self.__ev = 65535

        data = db.select(f'SELECT name, type1, type2, hp, attack, defense, special, speed FROM pokemon WHERE id = '
                         f'{pokemon_id};')[0]

        self.__name = data[0]
        self.__type1 = data[1]
        self.__type2 = data[2]
        self.__max_hp = self.__determine_stat(data[3]) + self.__level + 10
        self.__hp = self.__max_hp

        self.__base_atk = data[4]
        self.__base_def = data[5]
        self.__base_spc = data[6]
        self.__base_spe = data[7]

        self.__attack = self.__determine_stat(data[4]) + 5
        self.__defense = self.__determine_stat(data[5]) + 5
        self.__special = self.__determine_stat(data[6]) + 5
        self.__speed = self.__determine_stat(data[7]) + 5

        self.__moves = []
        self.__last_move = None
        self.__status_effect = enums.StatusEffect.NONE
        self.__sleep_counter = 0
        self.__confused = False
        self.__battle_atk = 0
        self.__battle_def = 0
        self.__battle_spc = 0
        self.__battle_spe = 0
        self.__accuracy = 0
        self.__evasion = 0
        self.__sub = None

    def __determine_stat(self, base):
        a = (base + self.__dv) * 2
        b = math.ceil(math.sqrt(self.__ev))
        b = math.floor(b / 4)
        return math.floor(((a + b) * self.__level) / 100)

    def add_move(self, move):
        if len(self.__moves) >= 4:
            return False
        self.__moves.append(move)

    def reset_battle_stats(self):
        self.__battle_atk = 0
        self.__battle_def = 0
        self.__battle_spc = 0
        self.__battle_spe = 0
        self.__accuracy = 0
        self.__evasion = 0

    def take_damage(self, damage):
        """ pokemon takes damage by given amount """
        self.__hp -= damage
        if self.__hp <= 0:
            self.__hp = 0
            self.publish(f'{self.__name} fainted.')

    def heal(self, health):
        """ heals pokemon by given amount """
        self.__hp += health
        if self.__hp > self.__max_hp:
            self.__hp = self.__max_hp

    def add_subscriber(self, subscriber):
        self.__sub = subscriber
        for move in self.__moves:
            move.add_subscriber(subscriber)

    def remove_subscriber(self):
        self.__sub = None
        for move in self.__moves:
            move.remove_subscriber()

    def publish(self, message):
        self.__sub.update(message)

    def get_move(self, itr):
        if itr not in range(0, 4):
            return None
        return self.__moves[itr]

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
    def status_effect(self):
        return self.__status_effect

    @property
    def confused(self):
        return self.__confused

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
        return self.__battle_stat(self.__accuracy)

    @property
    def evasion(self):
        return self.__battle_stat(self.__evasion)

    def __battle_stat(self, stage):
        """ stage is the battle stat to be calculated as a floating point value
         increasing and decreasing a stat has diminishing returns """
        num = 2
        den = 2

        if stage >= 0:
            num += stage
        else:
            den += stage

        return num / den

    def __str__(self):
        return f'Lv. {self.__level} {self.__name}\n{self.__hp} / {self.__max_hp}'
