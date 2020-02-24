import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from a_star import Position, GridPositionInfo, AStarSearch

class FloodNode:
    def __init__(self, position, colour='white'):
        self.position = position
        self.colour = colour

    def to_string(self):
        print('(' + str(self.position.x) + ',' + str(self.position.y) + ') - ' + self.colour)

class FloodGrid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[FloodNode(Position(x,y)) for x in range(width)] for y in range(height)]

    def insert(self, node):
        if (node.position.x < 0 or node.position.x > self.width):
            print('index out of range at x=' + str(node.position.x))
        if (node.position.y < 0 or node.position.y > self.height):
            print('index out of range at y=' + str(node.position.y))
        self.grid[node.position.x][node.position.y] = node

    def print_string(self):
        for i in range(self.width):
            for j in range(self.height):
                node = self.grid[j][i]
                print(node.colour, end=' ')
            print()

    def to_string(self):
        out_str = ''
        for i in range(self.width):
            for j in range(self.height):
                node = self.grid[j][i]
                out_str = out_str + node.colour + ' '
            out_str = out_str + '\n'
        return out_str

    def get_node_at(self, x, y):
        if (x >= 0 and x < self.width and y >= 0 and y < self.height):
            return self.grid[y][x]
        else:
            print('grid index out of range for ' + str(x) + ',' + str(y))
            return

    def count_red(self):
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.grid[i][j].colour == 'red'):
                    counter = counter + 1
        return counter

    def count_blue(self):
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.grid[i][j].colour == 'blue'):
                    counter = counter + 1
        return counter

    def count_yellow(self):
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.grid[i][j].colour == 'yellow'):
                    counter = counter + 1
        return counter

    def count_green(self):
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.grid[i][j].colour == 'green'):
                    counter = counter + 1
        return counter

    def count_white(self):
        counter = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.grid[i][j].colour == 'white'):
                    counter = counter + 1
        return counter

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

def flood_fill_left(node, target_colour, replace_colour):
    global floodGrid
    if (floodGrid is None):
        print('error retrieving floodGrid')
        return 
    if (check_for_obstacle(data, node.position)):
        node.colour = 'black'
        floodGrid.insert(node)
        print('found an obstacle')
        return
    if (target_colour == replace_colour):
        return  
    if (floodGrid.get_node_at(node.position.x, node.position.y).colour != target_colour):
        print('node is not target colour')
        return
    if (not check_for_obstacle(data, get_position_to_left(node.position))):
        westNode = FloodNode(get_position_to_left(node.position), 'yellow')
        print('westNode: ')
        westNode.to_string()
        floodGrid.insert(westNode)
        flood_fill_left(westNode, target_colour, replace_colour)
    return

def flood_fill_right(node, target_colour, replace_colour):
    global floodGrid
    if (floodGrid is None):
        print('error retrieving floodGrid')
        return 
    if (check_for_obstacle(data, node.position)):
        node.colour = 'black'
        floodGrid.insert(node)
        print('found an obstacle')
        return
    if (target_colour == replace_colour):
        return  
    if (floodGrid.get_node_at(node.position.x, node.position.y).colour != target_colour):
        print('node is not target colour')
        return
    if (not check_for_obstacle(data, get_position_to_right(node.position))):
        eastNode = FloodNode(get_position_to_right(node.position), 'red')
        print('eastNode:')
        eastNode.to_string()
        floodGrid.insert(eastNode)
        flood_fill_right(eastNode, target_colour, replace_colour)
    return

def flood_fill_up(node, target_colour, replace_colour):
    global floodGrid
    if (floodGrid is None):
        print('error retrieving floodGrid')
        return 
    if (check_for_obstacle(data, node.position)):
        node.colour = 'black'
        floodGrid.insert(node)
        print('found an obstacle')
        return
    if (target_colour == replace_colour):
        return  
    if (floodGrid.get_node_at(node.position.x, node.position.y).colour != target_colour):
        print('node is not target colour')
        return
    if (not check_for_obstacle(data, get_position_above(node.position))):
        northNode = FloodNode(get_position_above(node.position), 'blue')
        print('northNode:')
        northNode.to_string()
        floodGrid.insert(northNode)
        flood_fill_up(northNode, target_colour, replace_colour)
    return

def flood_fill_below(node, target_colour, replace_colour):
    global floodGrid
    if (floodGrid is None):
        print('error retrieving floodGrid')
        return 
    if (check_for_obstacle(data, node.position)):
        node.colour = 'black'
        floodGrid.insert(node)
        print('found an obstacle')
        return
    if (target_colour == replace_colour):
        return  
    if (floodGrid.get_node_at(node.position.x, node.position.y).colour != target_colour):
        print('node is not target colour')
        return
    if (not check_for_obstacle(data, get_position_below(node.position))):
        southNode = FloodNode(get_position_below(node.position), 'green')
        print('southNode:')
        southNode.to_string()
        floodGrid.insert(southNode)
        flood_fill_below(southNode, target_colour, replace_colour)
    return

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

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    global floodGrid
    global data
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))

    my_snake_head = Position(data['you']['body'][0]['x'], data['you']['body'][0]['y'])
    food = Position(data['board']['food'][0]['x'], data['board']['food'][0]['y'])
    #astar = AStarSearch(data['board']['height'], my_snake_head, food)
    floodGrid = FloodGrid(data['board']['width'], data['board']['height'])

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

    if (direction not in possible_directions):
        flood_fill_left(FloodNode(get_position_to_left(my_snake_head)), 'white', 'yellow')
        flood_fill_right(FloodNode(get_position_to_right(my_snake_head)), 'white', 'red')
        flood_fill_up(FloodNode(get_position_above(my_snake_head)), 'white', 'blue')
        flood_fill_below(FloodNode(get_position_below(my_snake_head)), 'white', 'green')

        flood_fill_values = [floodGrid.count_yellow(), 
                             floodGrid.count_red(),
                             floodGrid.count_blue(),
                             floodGrid.count_green()]
        biggest_space = flood_fill_values.index(max(flood_fill_values))
        direction = 'left' if biggest_space == 0 else 'right' if biggest_space == 1 else 'up' if biggest_space == 2 else 'down'

    #print(astar)

    return move_response(direction)


@bottle.post('/end')
def end():
    global floodGrid
    data = bottle.request.json
    end_grid_file = open("Death_grid.txt", "w")
    end_grid_file.write(floodGrid.to_string())
    end_grid_file.close()
    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

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
