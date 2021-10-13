import database.database as db
import math
import enums


class Pokemon:
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

    def print(self):
        print(f'{self.__name}\t Lv. {self.__level}')
        print(f'{self.__hp} / {self.__hp}')

    def __determine_stat(self, base):
        a = (base + self.__dv) * 2
        b = math.ceil(math.sqrt(self.__ev))
        b = math.floor(b / 4)
        return math.floor(((a + b) * self.__level) / 100)

    def reset_battle_stats(self):
        self.__battle_atk = 0
        self.__battle_def = 0
        self.__battle_spc = 0
        self.__battle_spe = 0
        self.__accuracy = 0
        self.__evasion = 0

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
        return self.__battle_atk

    @property
    def battle_def(self):
        return self.__battle_def

    @property
    def battle_spc(self):
        return self.__battle_spc

    @property
    def battle_spe(self):
        return self.__battle_spe

    @property
    def accuracy(self):
        return self.__accuracy

    @property
    def evasion(self):
        return self.__evasion
