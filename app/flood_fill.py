from a_star import Position
from helpers import *

class FloodNode:
    def __init__(self, position, colour='white'):
        self.position = position
        self.colour = colour

    # def to_string(self):
    #     print('(' + str(self.position.x) + ',' + str(self.position.y) + ') - ' + self.colour)

class FloodGrid:
    def __init__(self, data):
        self.height = data['board']['height']
        self.width = data['board']['width']
        self.grid = [[FloodNode(Position(x,y)) for x in range(self.width)] for y in range(self.height)]
        self.data = data
        self.blue_count = 0
        self.green_count = 0
        self.yellow_count = 0
        self.red_count = 0

    def insert(self, node):
        # if (node.position.x < 0 or node.position.x > self.width):
        #     print('index out of range at x=' + str(node.position.x))
        # if (node.position.y < 0 or node.position.y > self.height):
        #     print('index out of range at y=' + str(node.position.y))
        self.grid[node.position.x][node.position.y] = node

    # def print_string(self):
    #     for i in range(self.width):
    #         for j in range(self.height):
    #             node = self.grid[j][i]
    #             print(node.colour, end=' ')
    #         print()

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
            # print('grid index out of range for ' + str(x) + ',' + str(y))
            return

    def get_direction_of_biggest_space(self):
        flood_fill_values = [self.yellow_count, 
                             self.red_count,
                             self.blue_count,
                             self.green_count]
        biggest_space = flood_fill_values.index(max(flood_fill_values))
        ff_direction = 'left' if biggest_space == 0 else 'right' if biggest_space == 1 else 'up' if biggest_space == 2 else 'down'
        return ff_direction

    def flood_fill_left(self, node):
        if (check_for_obstacle(self.data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            node.colour = 'yellow'
            self.insert(node)
            self.yellow_count = self.flood_fill(node, 'yellow', 1)    
        return

    def flood_fill_right(self, node):
        if (check_for_obstacle(self.data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            node.colour = 'red'
            self.insert(node)
            self.red_count = self.flood_fill(node, 'red', 1)
        return

    def flood_fill_up(self, node):
        if (check_for_obstacle(self.data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            node.colour = 'blue'
            self.insert(node)
            self.blue_count = self.flood_fill(node, 'blue', 1)
        return

    def flood_fill_below(self, node):
        if (check_for_obstacle(self.data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            node.colour = 'green'
            self.insert(node)
            self.green_count = self.flood_fill(node, 'green', 1)
        return

    # the 'node' given as parameter has already been inserted into the grid
    def flood_fill(self, node, replace_colour, counter):
        left_pos = get_position_to_left(node.position)
        right_pos = get_position_to_right(node.position)
        up_pos = get_position_above(node.position)
        below_pos = get_position_below(node.position)

        westNode = self.get_node_at(left_pos.x, left_pos.y)
        if (westNode is not None):
            counter += self.flood_fill_node(westNode, replace_colour, 0)

        northNode = self.get_node_at(up_pos.x, up_pos.y)
        if (northNode is not None):
            counter += self.flood_fill_node(northNode, replace_colour, 0)

        eastNode = self.get_node_at(right_pos.x, right_pos.y)
        if (eastNode is not None):
            counter += self.flood_fill_node(eastNode, replace_colour, 0)

        southNode = self.get_node_at(below_pos.x, below_pos.y)
        if (southNode is not None):
            counter += self.flood_fill_node(southNode, replace_colour, 0)

        return counter

    def flood_fill_node(self, node, replace_colour, counter):
        if (node.colour == 'white' and not check_for_obstacle(self.data, node.position)):
            node.colour = replace_colour
            counter += 1
        elif (node.colour == 'white'):  # there must have been an obstacle
            node.colour = 'black'
            return counter
        elif (node.colour == 'black'):
            return counter
        elif (node.colour != replace_colour): # this space has already been visited from another direction
            node.colour = replace_colour
            counter += 1
        self.insert(node)
        # self.flood_fill(node, replace_colour, counter)
        return counter
