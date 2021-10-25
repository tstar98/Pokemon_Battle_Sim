from moves.move import *
from pokemon import *
from enums import MoveType


move_list = db.select('SELECT name, move_type FROM moves;')
moves = dict(move_list)
# select returns list of tuples, need to convert to list
move_list = db.select('SELECT name FROM stat_altering_moves;')
stat_alt_moves = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM stat_altering_attacks;')
stat_alt_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM multi_attacks;')
multi_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM flinch_attacks;')
flinch_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM status_effect_attacks;')
stat_eff_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM status_effect_moves;')
stat_eff_moves = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM confusing_attacks;')
conf_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM recoil_attacks;')
recoil = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM set_damage_attacks;')
set_dmg_atk = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM screen_moves;')
screen_moves = [move[0] for move in move_list]
move_list = db.select('SELECT name FROM confusing_continuous_attacks;')
conf_cont_moves = [move[0] for move in move_list]


def is_sam(move):
    return moves[move] == MoveType.STAT_ALT_MOVE.value and move in stat_alt_moves


def is_saa(move):
    return moves[move] == MoveType.STAT_ALT_ATK.value and move in stat_alt_atk


def is_multi(move):
    return moves[move] == MoveType.MULTI_ATK.value and move in multi_atk


def is_flinch(move):
    return moves[move] == MoveType.FLINCH_ATK.value and move in flinch_atk


def is_sea(move):
    return moves[move] == MoveType.STAT_EFF_ATK.value and move in stat_eff_atk


def is_sem(move):
    return moves[move] == MoveType.STAT_EFF_MOVE.value and move in stat_eff_moves


def is_ca(move):
    return moves[move] == MoveType.CONF_ATK.value and move in conf_atk


def is_recoil(move):
    return moves[move] == MoveType.RECOIL_ATK.value and move in recoil


def is_sda(move):
    return moves[move] == MoveType.SET_DMG_ATK.value and move in set_dmg_atk


def is_screen(move):
    return moves[move] == MoveType.SCREEN_MOVE.value and move in screen_moves


def is_cca(move):
    return moves[move] == MoveType.CONF_CONT_ATK.value and move in conf_cont_moves


def test_move_types():
    """Tests that all moves have the correct move type assignment and are in the correct db table"""

    assert moves['Absorb'] == MoveType.HEALING_ATK.value
    assert is_saa('Acid')
    assert is_sam('Acid Armor')
    assert is_sam('Agility')
    assert is_sam('Amnesia')
    assert is_saa('Aurora Beam')
    assert is_multi('Barrage')
    assert is_sam('Barrier')
    assert 'Bide' not in moves
    assert moves['Bind'] == MoveType.TRAP_ATK.value
    assert is_flinch('Bite')
    assert is_sea('Blizzard')
    assert is_sea('Body Slam')
    assert is_flinch('Bone Club')
    assert is_multi('Bonemerang')
    assert is_saa('Bubble')
    assert is_saa('Bubble Beam')
    assert moves['Clamp'] == MoveType.TRAP_ATK.value
    assert is_multi('Comet Punch')
    assert moves['Confuse Ray'] == MoveType.CONF_MOVE.value
    assert is_ca('Confusion')
    assert is_saa('Constrict')
    assert 'Conversion' not in moves
    assert 'Counter' not in moves
    assert moves['Crabhammer'] == MoveType.CRIT_ATK.value
    assert moves['Cut'] == MoveType.ATTACK.value
    assert is_sam('Defense Curl')
    assert moves['Dig'] == MoveType.VANISH_ATK.value
    assert 'Disable' not in moves
    assert is_ca('Dizzy Punch')
    assert is_multi('Double Kick')
    assert is_multi('Double Slap')
    assert is_sam('Double Team')
    assert is_recoil('Double-Edge')
    assert is_sda('Dragon Rage')
    assert moves['Dream Eater'] == MoveType.DREAM_EATER.value
    assert moves['Drill Peck'] == MoveType.ATTACK.value
    assert moves['Earthquake'] == MoveType.ATTACK.value
    assert moves['Egg Bomb'] == MoveType.ATTACK.value
    assert is_sea('Ember')
    assert moves['Explosion'] == MoveType.SELF_DESTR.value
    assert is_sea('Fire Blast')
    assert is_sea('Fire Punch')
    assert moves['Fire Spin'] == MoveType.TRAP_ATK.value
    assert is_sda('Fissure')
    assert is_sea('Flamethrower')
    assert is_sam('Flash')
    assert moves['Fly'] == MoveType.VANISH_ATK.value
    assert 'Focus Energy' not in moves
    assert is_multi('Fury Attack')
    assert is_multi('Fury Swipes')
    assert is_sem('Glare')
    assert is_sam('Growth')
    assert is_sda('Guillotine')
    assert moves['Gust'] == MoveType.ATTACK.value
    assert is_sam('Harden')
    assert 'Haze' not in moves
    assert is_flinch('Headbutt')
    assert moves['High Jump Kick'] == MoveType.MISS_RECOIL.value
    assert moves['Horn Attack'] == MoveType.ATTACK.value
    assert is_sda('Horn Drill')
    assert moves['Hydro Pump'] == MoveType.ATTACK.value
    assert moves['Hyper Beam'] == MoveType.RECHARGE_ATK.value
    assert is_flinch('Hyper Fang')
    assert is_sem('Hypnosis')
    assert is_sea('Ice Beam')
    assert is_sea('Ice Punch')
    assert moves['High Jump Kick'] == MoveType.MISS_RECOIL.value
    assert moves['Karate Chop'] == MoveType.CRIT_ATK.value
    assert is_sam('Kinesis')
    assert moves['Leech Life'] == MoveType.HEALING_ATK.value
    assert 'Leech Seed' not in moves
    assert is_sam('Leer')
    assert is_sea('Lick')
    assert is_screen('Light Screen')
    assert is_sem('Lovely Kiss')
    assert is_flinch('Low Kick')
    assert is_sam('Meditate')
    assert moves['Mega Drain'] == MoveType.HEALING_ATK.value
    assert moves['Mega Kick'] == MoveType.ATTACK.value
    assert moves['Mega Punch'] == MoveType.ATTACK.value
    assert moves['Metronome'] == MoveType.RANDOM.value
    assert moves['Mimic'] == MoveType.MIMIC_MOVE.value
    assert is_sam('Minimize')
    assert moves['Mirror Move'] == MoveType.MIRROR_MOVE.value
    assert 'Mist' not in moves
    assert is_sda('Night Shade')
    assert moves['Pay Day'] == MoveType.ATTACK.value
    assert moves['Peck'] == MoveType.ATTACK.value
    assert is_cca('Petal Dance')
    assert is_multi('Pin Missile')
    assert is_sem('Poison Gas')
    assert is_sem('Poison Powder')
    assert is_sea('Poison Sting')
    assert moves['Pound'] == MoveType.ATTACK.value
    assert is_ca('Psybeam')
    assert is_saa('Psychic')
    assert is_sda('Psywave')
    assert moves['Quick Attack'] == MoveType.ATTACK.value
    assert 'Rage' not in moves



def test_database():
    test_move_types()


if __name__ == '__main__':
    test_database()
