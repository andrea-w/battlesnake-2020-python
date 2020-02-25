from app.a_star import Position

def get_position_to_left(pos):
    return Position(pos.x - 1, pos.y)

def get_position_to_right(pos):
    return Position(pos.x + 1, pos.y)

def get_position_above(pos):
    return Position(pos.x, pos.y - 1)

def get_position_below(pos):
    return Position(pos.x, pos.y + 1)

def get_position_for_move_command(move, current_pos):
    if (move == 'left'):
        return get_position_to_left(current_pos)
    elif (move == 'right'):
        return get_position_to_right(current_pos)
    elif (move == 'up'):
        return get_position_above(current_pos)
    else:
        return get_position_below(current_pos)

def position_of_nearest_food(data):
    my_snake_head = get_my_head_pos()
    min_crumb_dist = 999
    for crumb in data['board']['food']:
        crumb_dist = get_manhattan_distance_between(crumb, my_snake_head)
        if min_crumb_dist > crumb_dist:
            min_crumb_dist = crumb_dist
            nearest_food = Position(crumb)
    return nearest_food or None

def get_directions_to_goal(current, goal):
    directions = []
    if (current.x > goal.x):
        directions.append('left')
    if (current.x < goal.x):
        directions.append('right')
    if (current.y < goal.y):
        directions.append('down')
    if (current.y > goal.y):
        directions.append('up')
    return directions

def get_directions_away_from(current, avoid):
    distance = get_manhattan_distance_between(current, avoid)
    possible_directions = get_possible_directions()
    # iterate through possible_directions; remove away that decrease manhattan distance between us and opponent
    for dir in possible_directions:
        pos = get_position_for_move_command(dir, current)
        if (get_manhattan_distance_between(pos, avoid) <= distance):
            possible_directions.remove(dir)
    return possible_directions

def get_manhattan_distance_between(a,b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def check_for_obstacle(data, position):
    walls = {
        'up': -1,
        'left': -1,
        'down': data['board']['height'],
        'right': data['board']['width']
    }

    for snake in data['board']['snakes']:
        for piece in snake['body']:
            if (piece['x'] == position.x and piece['y'] == position.y):
                return True
    
    if walls['up'] == position.y or walls['down'] == position.y or walls['left'] == position.x or walls['right'] == position.x:
        return True

    return False

def opponent_snake_head_nearby(my_snake_head, snake):
    if (get_manhattan_distance_between(my_snake_head, Position(snake['body'][0]['x'], snake['body'][0]['y'])) <= 2):
        return True
    else:
        return False

def get_my_head_pos(data):
    return Position(data['you']['body'][0]['x'], data['you']['body'][0]['y'])

def get_possible_directions(data):
    my_snake_head = get_my_head_pos(data)
    obstacle_flag = {
        'up': check_for_obstacle(data, get_position_above(my_snake_head)),
        'right': check_for_obstacle(data, get_position_to_right(my_snake_head)),
        'down': check_for_obstacle(data, get_position_below(my_snake_head)),
        'left': check_for_obstacle(data, get_position_to_left(my_snake_head))
    }

    possible_directions = []
    if not obstacle_flag['up']:
        possible_directions.append('up')
    if not obstacle_flag['right']:
        possible_directions.append('right')
    if not obstacle_flag['left']:
        possible_directions.append('left')
    if not obstacle_flag['down']:
        possible_directions.append('down')

    return possible_directions