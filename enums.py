from enum import Enum


class Type(Enum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    GRASS = 3
    ELECTRIC = 4
    ICE = 5
    FIGHTING = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14


class StatusEffect(Enum):
    PARALYSIS = 0
    SLEEP = 1
    BURN = 2
    FREEZE = 3
    POISON = 4
    BAD_POISON = 5
    NONE = 6


class Barrier(Enum):
    REFLECT = 0
    LIGHT = 1


class Stat(Enum):
    ATTACK = 0
    DEFENSE = 1
    SPECIAL = 2
    SPEED = 3
    ACCURACY = 4
    EVASION = 5


class MoveType(Enum):
    ATTACK = 0
    STAT_ALT_ATK = 1
    SET_DMG_ATK = 2
    FLINCH_ATK = 3
    RECOIL_ATK = 4
    MISS_RECOIL = 5
    STAT_EFF_ATK = 6
    CONT_ATK = 7
    MULT_CONT_ATK = 8
    CONF_CONT_ATK = 9
    HEALING_ATK = 10
    CHARGE_ATK = 11

    SCREEN_MOVE = 12
    SWITCHING_MOVE = 13
    STAT_ALT_MOVE = 14
    STAT_EFF_MOVE = 15
    HEALING_MOVE = 16
    SELF_STAT_ALT = 17
    CONF_MOVE = 18
    RANDOM = 19

    MULTI_ATK = 20
    TRAP_ATK = 21
    CONF_ATK = 22
    CRIT_ATK = 23
    VANISH_ATK = 24
    DREAM_EATER = 25
    SELF_DESTR = 26
    RECHARGE_ATK = 27

    MIMIC_MOVE = 28
    REST = 29
    SELF_SWITCH_MOVE = 30
    STAT_CHARGE_ATK = 31
    SPLASH = 32
    SKY_GROUND_ATK = 33
    TRANSFORM = 34

    STRUGGLE = 35
    MIRROR_MOVE = 36
