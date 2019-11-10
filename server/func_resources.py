import random
from json import dumps
import math

from server.db_models.db import db
from server.db_models.Character import Character
from server.db_models.Blueprint import Blueprint


# Character table
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | id           | int(11)      | NO   | PRI | NULL    | auto_increment |
# | char_name    | varchar(45)  | NO   | UNI | NULL    |                |
# | health       | int(11)      | NO   |     | NULL    |                |
# | strength     | int(11)      | NO   |     | NULL    |                |
# | reflex       | int(11)      | NO   |     | NULL    |                |
# | charisma     | int(11)      | NO   |     | NULL    |                |
# | intelligence | int(11)      | NO   |     | NULL    |                |
# | will         | int(11)      | NO   |     | NULL    |                |
# | user_id      | int(11)      | NO   | UNI | NULL    |                |
# | img_path     | varchar(128) | NO   |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+

# Blueprint table
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | id           | int(11)      | NO   | PRI | NULL    | auto_increment |
# | type         | int(11)      | NO   |     | NULL    |                |
# | health       | int(11)      | NO   |     | NULL    |                |
# | strength     | int(11)      | NO   |     | NULL    |                |
# | reflex       | int(11)      | NO   |     | NULL    |                |
# | charisma     | int(11)      | NO   |     | NULL    |                |
# | intelligence | int(11)      | NO   |     | NULL    |                |
# | will         | int(11)      | NO   |     | NULL    |                |
# | armor        | int(11)      | NO   |     | NULL    |                |
# | min_dmg      | int(11)      | NO   |     | NULL    |                |
# | max_dmg      | int(11)      | NO   |     | NULL    |                |
# | img_path     | varchar(128) | NO   |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+


def calculate_stats(char):
    """

    :param char:
    :return:
    """
    if isinstance(char, str):
        char = Character.query.filter_by(name=char).first()
    elif isinstance(char, int):
        char = Character.query.filter_by(id=char).first()
    char_stats = char.to_dict_stats()
    items = char_stats.pop('items_in_game')
    items = [item.to_dict() for item in items]
    item_stats = []
    for item in items:
        if item['equipped']:
            stats = Blueprint.query.filter_by(id=item['bp_id']).first().to_dict_stats()
            item_stats.append(stats)
    for item in item_stats:
        for stat, value in item.items():
            if stat in char_stats.keys():
                char_stats[stat] += value
            else:
                char_stats[stat] = value
    return char_stats


def calc_damage(attacker={}, defender={}):
    damage = (0.4 * attacker['strength']) + (0.3 * attacker['reflex']) + (0.2 * attacker['intelligence'])
    dice = random.randint(0, 100)
    reflex_diff = abs(defender['reflex'] - attacker['reflex'])
    dodge = False
    critical = False
    if attacker['luck'] >= dice:
        critical = True
        damage *= 2

    if dice < reflex_diff:
        dodge = True
        return 0, critical, dodge
    damage -= (0.1 * defender['armor'])
    if damage > 1:
        return math.ceil(damage), critical, dodge
    else:
        return 1, critical, dodge


def run_arena_fight(a_char, d_char, dump_data=True):
    attacker = calculate_stats(a_char)
    defender = calculate_stats(d_char)
    print("ATTTAAAAAAAAAAAACKER:", attacker)
    print("DEFEENDEEEEEEEEEER:", defender)
    # Don't let someone attack with such low health pool,
    # defenders health is not important - it is not finally taken away
    if attacker['health'] <= 30:
        health_diff = str(31 - attacker['health'])
        response = {
            'success': False,
            'message': 'Not enough health to fight.',
            'additional_info': 'You need {0} more health to fight.'.format(health_diff)
        }
        return response

    # The actual fight once it starts
    response = {
        'success': True,
        'winner': bool(),
        'attacker_health': attacker['health'],
        'rounds': []
    }
    attacker.update({'luck': random.randint(0, 15)})
    defender.update({'luck': random.randint(0, 10)})
    att_total_damage = 0
    def_total_damage = 0
    rounds = 0
    while True:
        rounds += 1
        att_damage, att_critical, att_dodge = calc_damage(attacker=attacker, defender=defender)
        att_total_damage += att_damage
        def_damage, def_critical, def_dodge = calc_damage(attacker=defender, defender=attacker)
        def_total_damage += att_damage
        round_desc = {
            'number': rounds,
            'attacker_damage': att_damage,
            'attacker_critical': att_critical,
            'attacker_dodge': att_dodge,
            'defender_damage': def_damage,
            'defender_critical': def_critical,
            'defender_dodge': def_dodge,
        }
        response['rounds'].append(round_desc)

        if defender['health'] <= att_total_damage:
            response.update({'winner': True})
            break

        if attacker['health'] <= def_damage:
            response.update({'winner': False})
            break
    response['attacker_health'] -= int(0.15 * def_total_damage)
    attacker_char = Character.query.filter_by(id=a_char).first()
    attacker_char.edit(health=response['attacker_health'])
    # print(db.session.query(Character).count())
    db.session.commit()
    return response


def run_expedition_fight(a_char, enemy, dump_data=True):
    attacker = calculate_stats(a_char)
    enemy = calculate_stats(enemy)
    print("ATTTAAAAAAAAAAAACKER:", attacker)
    print("DEFEENDEEEEEEEEEER:", enemy)
    # Don't let someone attack with such low health pool,
    # defenders health is not important - it is not finally taken away
    if attacker['health'] <= 30:
        health_diff = str(31 - attacker['health'])
        response = {
            'success': False,
            'message': 'Not enough health to fight.',
            'additional_info': 'You need {0} more health to fight.'.format(health_diff)
        }
        return response

    # The actual fight once it starts
    response = {
        'success': True,
        'winner': bool(),
        'attacker_health': attacker['health'],
        'rounds': []
    }
    attacker.update({'luck': random.randint(0, 15)})
    enemy.update({'luck': 0})
    att_total_damage = 0
    def_total_damage = 0
    rounds = 0
    while True:
        rounds += 1
        att_damage, att_critical, att_dodge = calc_damage(attacker=attacker, defender=enemy)
        att_total_damage += att_damage
        def_damage, def_critical, def_dodge = calc_damage(attacker=enemy, defender=attacker)
        def_total_damage += att_damage
        round_desc = {
            'number': rounds,
            'attacker_damage': att_damage,
            'attacker_critical': att_critical,
            'attacker_dodge': att_dodge,
            'defender_damage': def_damage,
            'defender_critical': def_critical,
            'defender_dodge': def_dodge,
        }
        response['rounds'].append(round_desc)

        if enemy['health'] <= att_total_damage:
            response.update({'winner': True})
            break

        if attacker['health'] <= def_damage:
            response.update({'winner': False})
            break
    response['attacker_health'] -= int(0.15 * def_total_damage)
    attacker_char = Character.query.filter_by(id=a_char).first()
    attacker_char.edit(health=response['attacker_health'])
    # print(db.session.query(Character).count())
    db.session.commit()
    return response