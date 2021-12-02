import sqlite3 as sql
import os.path
from Pokemon_Battle_Sim import enums


# need to use this to call functions from outside of package
dir_path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(dir_path, 'pokemon.db')
con = sql.connect(db)


def select(query):
    return con.execute(query).fetchall()


def create_tables():
    with con:
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY, name TEXT, type1 TEXT, type2 TEXT, '
        #     'total INTEGER, hp INTEGER, attack INTEGER, defense INTEGER, special INTEGER, speed INTEGER);'
        # )
        #
        # file = open('pokemon.csv', encoding='utf8')
        #
        # for line in file:
        #     d = line.split(',')
        #
        #     con.execute(
        #         'INSERT INTO pokemon VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
        #         (int(d[0]), d[1], d[2].upper(), None if d[3] == '' else d[3].upper(), int(d[4]), int(d[5]), int(d[6]),
        #          int(d[7]), int(d[8]), int(d[9]))
        #     )
        #
        # file.close()
        # file = open('moves.csv', encoding='utf8')
        #
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS moves (name TEXT PRIMARY KEY, type TEXT, category TEXT, power INTEGER, '
        #     'accuracy INTEGER, pp INTEGER, priority INTEGER, description TEXT, move_type INTEGER);'
        # )
        #
        # for line in file:
        #     d = line.split(',')
        #     if '#' in line[0]:
        #         continue
        #
        #     con.execute(
        #         'INSERT INTO moves VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);',
        #         (d[1], d[2], d[3], None if d[4] == '' else int(d[4]), None if d[5] == '' else int(d[5]),
        #          None if d[6] == '' else int(d[6]), 0, d[7], int(d[8].strip()))
        #     )
        # file = open('confusing_continuous_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS confusing_continuous_attacks (name TEXT PRIMARY KEY, min_hits INTEGER, '
        #     'max_hits INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO confusing_continuous_attacks VALUES (?, ?, ?);', (d[0], int(d[1]), int(d[2]))
        #     )
        # file.close()
        #
        # file = open('flinch_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS flinch_attacks (name TEXT PRIMARY KEY, chance INTEGER); '
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO flinch_attacks VALUES (?, ?);', (d[0], int(d[1]))
        #     )
        # file.close()
        #
        # file = open('multi_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS multi_attacks (name TEXT PRIMARY KEY, min_hits INTEGER, '
        #     'max_hits INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO multi_attacks VALUES (?, ?, ?);', (d[0], int(d[1]), int(d[2]))
        #     )
        # file.close()
        #
        # file = open('recoil_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO recoil_attacks VALUES (?, ?);', (d[0], int(d[1]))
        #     )
        # file.close()
        #
        # file = open('screen_moves.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS screen_moves (name TEXT PRIMARY KEY, screen_type INTEGER); '
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO screen_moves VALUES (?, ?);', (d[0], int(d[1]))
        #     )
        # file.close()
        #
        # file = open('set_damage_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS set_damage_attacks (name TEXT PRIMARY KEY, damage INTEGER); '
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO set_damage_attacks VALUES (?, ?);', (d[0], None if d[1].isspace()  else int(d[1]))
        #     )
        # file.close()
        #
        # file = open('stat_altering_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS stat_altering_attacks (name TEXT PRIMARY KEY, chance INTEGER, stat INTEGER,'
        #     'stages INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO stat_altering_attacks VALUES (?, ?, ?, ?);', (d[0], int(d[1]), int(d[2]), int(d[3]))
        #     )
        # file.close()
        #
        # file = open('stat_altering_moves.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS stat_altering_moves (name TEXT PRIMARY KEY, self BOOLEAN, stat INTEGER,'
        #     'stages INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO stat_altering_moves VALUES (?, ?, ?, ?);', (d[0], bool(d[1]), int(d[2]), int(d[3]))
        #     )
        # file.close()
        #
        # file = open('stat_charging_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS stat_charging_attacks (name TEXT PRIMARY KEY, stat INTEGER, '
        #     'stages INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO stat_charging_attacks VALUES (?, ?, ?);', (d[0], int(d[1]), int(d[2]))
        #     )
        # file.close()
        #
        # file = open('status_effect_attacks.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS status_effect_attacks (name TEXT PRIMARY KEY, chance INTEGER, '
        #     'status_effect INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO status_effect_attacks VALUES (?, ?, ?);', (d[0], int(d[1]), int(d[2]))
        #     )
        # file.close()
        #
        # file = open('status_effect_moves.csv', 'r')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS status_effect_moves (name TEXT PRIMARY KEY, status_effect INTEGER); '
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO status_effect_moves VALUES (?, ?);', (d[0], int(d[1]))
        #     )
        # file.close()

        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS attacks (name TEXT PRIMARY KEY);'
        # )
        # con.execute(
        #     'INSERT INTO attacks SELECT name FROM moves WHERE move_type = 0 OR move_type = 1 OR move_type = 2 '
        #     'OR move_type = 3 OR move_type = 4 OR move_type = 5 OR move_type = 6 OR move_type = 7 OR move_type = 8'
        #     ' OR move_type = 9 OR move_type = 1 OR move_type = 11 OR move_type = 20 OR move_type = 21 OR move_type = 22'
        #     ' OR move_type = 23 OR move_type = 24 OR move_type = 25 OR move_type = 26 OR move_type = 27'
        #     ' OR move_type = 31 OR move_type = 33'
        # )
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS status_moves(name TEXT PRIMARY KEY);'
        # )
        # con.execute(
        #     'INSERT INTO attacks SELECT name FROM moves WHERE move_type = 12 OR move_type = 13 OR move_type = 14'
        #     ' OR move_type = 15 OR move_type = 16 OR move_type = 17 OR move_type = 18 OR move_type = 19'
        #     ' OR move_type = 28 OR move_type = 29 OR move_type = 30 OR move_type = 32 OR move_type = 34'
        # )
        # con.execute('CREATE TABLE IF NOT EXISTS random(name TEXT PRIMARY KEY);')
        # con.execute(
        #     'INSERT INTO random SELECT name FROM moves WHERE name != \'Struggle\' AND name != \'Metronome\' '
        #     'AND name != \'Mimic\';'
        # )

        # file = open('confusing_attacks.csv')
        # con.execute(
        #     'CREATE TABLE IF NOT EXISTS confusing_attacks(name TEXT PRIMARY KEY, chance INTEGER);'
        # )
        # for line in file:
        #     d = line.split(',')
        #     con.execute(
        #         'INSERT INTO confusing_attacks VALUES(?,?);', (d[0], int(d[1]))
        #     )

        pass
    pass


def update_table(query):
    with con:
        con.execute(query)


def delete_table(table):
    with con:
        con.execute(f'DROP TABLE IF EXISTS {table}')


def create_csvs():
    # # create_tables()
    # file = open('stat_altering_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.STAT_ALT_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('set_damage_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.SET_DMG_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('recoil_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.RECOIL_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('status_effect_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.STAT_EFF_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('confusing_continuous_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.CONF_CONT_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('screen_moves.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.SCREEN_MOVE.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('stat_altering_moves.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.STAT_ALT_MOVE.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('status_effect_moves.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.STAT_EFF_MOVE.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('multi_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.MULTI_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')
    #
    # file.close()
    # file = open('stat_charging_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {Enums.MoveType.STAT_CHARGE_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')

    # file.close()
    # file = open('flinch_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = {enums.MoveType.FLINCH_ATK.value};')
    # for move in moves:
    #     file.write(f'{move[0]},\n')\

    # file.close()
    # file = open('confusing_attacks.csv', 'w')
    # moves = select(f'SELECT name FROM moves WHERE move_type = \'{enums.MoveType.CONF_ATK.value}\';')
    # for move in moves:
    #     file.write(f'{move[0]}\n')
    #
    # file.close()
    pass


if __name__ == '__main__':
    update_table("UPDATE moves SET description = 'A Psychic-type attack of varying intensity. It occasionally inflicts heavy damage.' WHERE name = 'Psywave'")

    print(select("SELECT * FROM set_damage_attacks"))
    print(select("SELECT * FROM moves WHERE move_type = 38"))
    print(select("SELECT * FROM moves WHERE move_type = 39"))
    pass
