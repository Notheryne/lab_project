import random
from json import dumps
import math

from server.db_models.db import db
from server.db_models.Character import Character
from server.db_models.ItemsInGame import ItemsInGame
from server.db_models.NonPersonCharacter import NonPersonCharacter
from server.db_models.Enemy import Enemy
from server.db_models.Blueprint import Blueprint


def calculate_stats(char_id, char=None):
    """

    Return character stats considering related items. Pass Character object or character id.
    :param char_id:
    :param char:
    :return: dict
    """
    if not char:
        if isinstance(char_id, str):
            char = Character.query.filter_by(name=char_id).first()
        elif isinstance(char_id, int):
            char = Character.query.filter_by(id=char_id).first()
    char_stats = char.to_dict_stats()
    items = char_stats.pop('items_in_game')
    items = [item.to_dict() for item in items]
    item_stats = []
    for item in items:
        stats = Blueprint.query.filter_by(id=item['bp_id']).first().to_dict_stats()
        item_stats.append(stats)
    for item in item_stats:
        for stat, value in item.items():
            if stat in char_stats.keys():
                char_stats[stat] += value
            else:
                char_stats[stat] = value
    return char_stats


def update_level(character, add_experience):
    """

    Add experience to character and calculate if it's enough for next level. If so, add 5 stat
    points. Each level requires (level - 1)_exp 8 1.8
    :param character: Character object
    :param add_experience: amount of experience to add (int)
    :return: None
    """
    character_stats = character.to_dict()
    start_level = character_stats['level']
    experience = character_stats['experience'] + add_experience
    thresholds = [100]
    i = 1
    while experience >= thresholds[-1]:
        print('Going', int(thresholds[i-1] * 1.8))
        thresholds.append(int(thresholds[i-1] * 1.8))
        i += 1
    level = len(thresholds)
    free_stats = (level - start_level) * 5
    character.edit(experience=experience, level=level, free_stats=free_stats)


def calc_damage(attacker=None, defender=None):
    """

    Calculate the amount of damage done.
    damage = x + (0.4 * s + 0.3 * r + 0.2 * i)
    where:
    x in [minimum damage, maximum damage]
    s - strength
    r - reflex
    i - intelligence
    :param attacker: Character or Enemy converted to dict
    :param defender: Character or Enemy converted to dict
    :return: tuple
    """
    damage = (0.4 * attacker['strength']) + (0.3 * attacker['reflex']) + (0.2 * attacker['intelligence'])
    damage += random.randint(attacker['min_dmg'], attacker['max_dmg'])
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


def run_fight(a_char, d_char=None, enemy=None, dump_data=True):
    """

    Simulate a fight based on attacker and deffender stats,
    return a result with the course of each round
    :param a_char: Character object
    :param d_char: Character object
    :param enemy: Enemy object
    :param dump_data: True to save data to file (useful for predicting result)
    :return: dict
    """
    attacker = calculate_stats(a_char)
    if d_char:
        defender = calculate_stats(d_char)
        defender.update({'luck': random.randint(0, 10)})
        experience = None
    elif enemy:
        enemy = Enemy.query.filter_by(id=enemy).first()
        defender = enemy.to_dict_stats()
        defender.update({'luck': 0})
        experience = defender.pop('experience')
    else:
        raise TypeError
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

        if attacker['health'] <= def_total_damage:
            response.update({'winner': False})
            break

    response['attacker_health'] -= int(0.15 * def_total_damage)
    attacker_char = Character.query.filter_by(id=a_char).first()
    attacker_char.edit(health=response['attacker_health'])
    if experience and response['winner']:
        update_level(attacker_char, experience)
        attacker_char.edit(gold=enemy['gold'])
    elif experience and not response['winner']:
        update_level(attacker_char, int(experience/10))
        attacker_char.edit(gold=int(enemy['gold'] * 0.4))

    db.session.commit()
    return response


def get_stats_npc(char_id, healer=False, trader=False):
    """

    Helper for getting stats of char and NPC's text
    :param char_id: int
    :param healer: bool
    :param trader: bool
    :return: tuple (Character, string)
    """
    char_id = int(char_id)
    char = Character.find_by_id(char_id, todict=True)
    npc = NonPersonCharacter.query.filter_by(healer=healer, trader=trader).first().to_dict()
    return char, npc['texts'][random.randint(0, len(npc['texts']))]
