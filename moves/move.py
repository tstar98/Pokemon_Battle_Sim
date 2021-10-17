import database.database as db
from enums import MoveType as mt


class Move:
    def __init__(self, name):
        move = db.select(f'SELECT type, power, accuracy, pp, priority, description FROM moves '
                         f'WHERE NAME = \'{name}\';')[0]
        self._name = name
        self._type, self._power, self._accuracy, self._max_pp, self._priority, self._desc = move
        self._pp = self._max_pp

    def use_move(self):
        pass

    def decrement_pp(self):
        self._pp -= 1

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def power(self):
        return self._power

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def max_pp(self):
        return self._max_pp

    @property
    def pp(self):
        return self._pp

    @property
    def priority(self):
        return self._priority

    @property
    def desc(self):
        return self._desc

    def __str__(self):
        return f'{self._name}\nPP = {self._pp} / {self._max_pp}'


def move_factory(name):
    from moves.attacks import Attack, StatAlteringAttack, SetDamageAttack, FlinchAttack, RecoilAttack, \
        RecoilOnMissAttack, StatusEffectAttack, ConfusingContinuousAttack, HealingAttack, ChargingAttack, MultiAttack, \
        TrapAttack, ConfusingAttack, CritAttack, VanishingAttack, DreamEater, SelfDestruct, RechargeAttack, \
        Struggle
    from moves.status_moves import ScreenMove, SwitchingMove, StatAlteringMove, StatusEffectMove, HealingMove, \
        ConfusingMove, RandomMove, MimicMove, Rest, Splash

    move_id = db.select(f'SELECT move_type FROM moves WHERE name = \'{name}\';')[0]

    moves = {
        mt.ATTACK.value: Attack,
        mt.STAT_ALT_ATK.value: StatAlteringAttack,
        mt.SET_DMG_ATK.value: SetDamageAttack,
        mt.FLINCH_ATK.value: FlinchAttack,
        mt.RECOIL_ATK.value: RecoilAttack,
        mt.MISS_RECOIL.value: RecoilOnMissAttack,
        mt.STAT_EFF_ATK.value: StatusEffectAttack,
        mt.CONF_CONT_ATK.value: ConfusingContinuousAttack,
        mt.HEALING_ATK.value: HealingAttack,
        mt.CHARGE_ATK.value: ChargingAttack,
        mt.MULTI_ATK.value: MultiAttack,
        mt.TRAP_ATK.value: TrapAttack,
        mt.CONF_ATK.value: ConfusingAttack,
        mt.CRIT_ATK.value: CritAttack,
        mt.VANISH_ATK.value: VanishingAttack,
        mt.DREAM_EATER.value: DreamEater,
        mt.SELF_DESTR.value: SelfDestruct,
        mt.RECHARGE_ATK.value: RechargeAttack,
        mt.STRUGGLE.value: Struggle,
        mt.SCREEN_MOVE.value: ScreenMove,
        mt.SWITCHING_MOVE.value: SwitchingMove,
        mt.STAT_ALT_MOVE.value: StatAlteringMove,
        mt.STAT_EFF_MOVE.value: StatusEffectMove,
        mt.HEALING_MOVE.value: HealingMove,
        mt.CONF_MOVE.value: ConfusingMove,
        mt.RANDOM.value: RandomMove,
        mt.MIMIC_MOVE.value: MimicMove,
        mt.REST.value: Rest,
        mt.SPLASH.value: Splash
    }
    return moves[move_id[0]](name)


def get_learnset(pokemon_id):
    file = open('csv/learnsets.csv', 'r')

    for line in file:
        info = line.split(',')
        if int(info[0]) == pokemon_id:
            return info[2:len(info)]
