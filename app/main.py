import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from a_star import Position, GridPositionInfo, AStarSearch

def get_position_to_left(pos):
    return Position(pos.x - 1, pos.y)

def get_position_to_right(pos):
    return Position(pos.x + 1, pos.y)

def get_position_above(pos):
    return Position(pos.x, pos.y - 1)

def get_position_below(pos):
    return Position(pos.x, pos.y + 1)

def position_of_nearest_food(data, current):
    min_crumb_dist = 999
    for crumb in data['board']['food']:
        crumb_dist = abs(crumb['x'] - current.x) + abs(crumb['y'] - current.y)
        if min_crumb_dist > crumb_dist:
            min_crumb_dist = crumb_dist
            nearest_food = Position(crumb['x'], crumb['y'])
    return nearest_food or None

def get_direction_to_goal(current, goal):
    if (current.x > goal.x):
        return 'left'
    elif (current.x < goal.x):
        return 'right'
    elif (current.y < goal.y):
        return 'down'
    elif (current.y > goal.y):
        return 'up'

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

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))
    my_snake_head = Position(data['you']['body'][0]['x'], data['you']['body'][0]['y'])
    food = Position(data['board']['food'][0]['x'], data['board']['food'][0]['y'])
    #astar = AStarSearch(data['board']['height'], my_snake_head, food)

    obstacle_flag = {
        'up': check_for_obstacle(data, get_position_above(my_snake_head)),
        'right': check_for_obstacle(data, get_position_to_right(my_snake_head)),
        'down': check_for_obstacle(data, get_position_below(my_snake_head)),
        'left': check_for_obstacle(data, get_position_to_left(my_snake_head))
    }

    target_food = position_of_nearest_food(data, my_snake_head)

    possible_directions = []
    if not obstacle_flag['up']:
        possible_directions.append('up')
    if not obstacle_flag['right']:
        possible_directions.append('right')
    if not obstacle_flag['left']:
        possible_directions.append('left')
    if not obstacle_flag['down']:
        possible_directions.append('down')

    direction = get_direction_to_goal(my_snake_head, target_food)
    print(direction)
    print(possible_directions)
    if (direction not in possible_directions):
        direction = possible_directions[random.randint(0, len(possible_directions) - 1)]

    #print(astar)


    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
