import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from a_star import Position, GridPositionInfo
from helpers import *
from flood_fill import *
from head_on_collision import *


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
    #print(json.dumps(data))

    return start_response("#33BEFF", "silly", "curled")


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))
    global floodGrid
    floodGrid = FloodGrid(data)
    my_snake_head = get_my_head_pos(data)


    target_food = position_of_nearest_food(data)
    food_directions = get_directions_to_goal(my_snake_head, target_food)

    collision_moves = get_moves_if_collision_possible(data)
    
    possible_directions = get_possible_directions(data)

    left_pos = get_position_to_left(my_snake_head)
    leftNode = floodGrid.get_node_at(left_pos.x, left_pos.y)
    if (leftNode is not None):
        floodGrid.flood_fill_left(leftNode)

    right_pos = get_position_to_right(my_snake_head)
    rightNode = floodGrid.get_node_at(right_pos.x, right_pos.y)
    if (rightNode is not None):
        floodGrid.flood_fill_right(rightNode)

    above_pos = get_position_above(my_snake_head)
    aboveNode = floodGrid.get_node_at(above_pos.x, above_pos.y)
    if (aboveNode is not None):
        floodGrid.flood_fill_up(aboveNode)

    below_pos = get_position_below(my_snake_head)
    belowNode = floodGrid.get_node_at(below_pos.x, below_pos.y)
    if (belowNode is not None):
        floodGrid.flood_fill_below(belowNode)

    if (collision_moves is not None):
        direction = collision_moves[0]
    else:
        directions = food_directions
        directions.append(floodGrid.get_direction_of_biggest_space())
        print(directions)
        direction = directions[random.randint(0, len(directions) - 1)]
        while (direction not in possible_directions):
            direction = directions[random.randint(0, len(directions) - 1)]
        print(direction)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json
    # end_grid_file = open("Death_grid.txt", "w")
    # end_grid_file.write(floodGrid.to_string())
    # end_grid_file.close()
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
