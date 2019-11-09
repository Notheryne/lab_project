import random
from json import dumps
import math


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

def calc_damage(strength, reflex, intelligence, luck):
    damage = 0.2 * strength
    damage += 0.15 * reflex
    damage += 0.1 * intelligence
    parameter = random.randint(100)
    if luck >= parameter:
        damage *= 2
    return math.ceil(damage)


def run_fight(attacker_name, defender, dump_data=True):

    # Don't let someone attack with such low health pool,
    # defenders health is not important - it is not finally taken away
    if a['health'] <= 50:
        health_diff = str(51 - a['health'])
        response = {
            'success': False,
            'message': 'Not enough health to fight.',
            'additional_info': 'You need {0} more health to fight.'.format(health_diff)
        }
        return dumps(response)

    # The actual fight once it starts
    else:
        a.update({'luck': random.randint(15)})
        b.update({'luck': random.randint(10)})




A = {
    'health': 100,
    'strength': 10,
    'reflex': 15,
    'charisma': 13,
    'intelligence': 20,
    'will': 30,
}

AW = {
    'min_dmg': 10,
    'max_dmg': 20,
}

B = {
    'health': 100,
    'strength': 12,
    'reflex': 32,
    'charisma': 21,
    'intelligence': 9,
    'will': 19,
}

BW = {
    'min_dmg': 3,
    'max_dmg': 9,
}

print(run_fight(A, B, AW, BW))