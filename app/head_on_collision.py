from a_star import Position
from helpers import *

def get_moves_if_collision_possible(data):
    my_id = data['you']['id']
    my_head_pos = Position(data['you']['body'][0]['x'], data['you']['body'][0]['y'])
    for snake in data['board']['snakes']:
        if snake['id'] != my_id:
            snake_head_pos = Position(snake['body'][0])
            if (get_manhattan_distance(my_head_pos, snake_head_pos) <= 2):
                return optimal_moves(data, snake)
    return None

def optimal_moves(data, snake):
    snake_head_pos = Position(snake['body'][0])
    my_head_pos = get_my_head_pos()
    if (am_i_bigger_than_opponent(data['you'], snake)):
        # enter attack mode
        dirs = get_directions_to_goal(my_head_pos, snake_head_pos)
        return list(set(dirs) & set(get_possible_directions()))[0]
    # else avoid opponent
    return get_directions_away_from(my_head_pos, snake_head_pos)

def get_manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def am_i_bigger_than_opponent(me, opponent):
    if (len(me['body']) > (1 + len(opponent['body']))):
        return True
    return False