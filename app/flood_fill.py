from app.a_star import Position
from app.helpers import *

class FloodNode:
    def __init__(self, position, colour='white'):
        self.position = position
        self.colour = colour

    def to_string(self):
        print('(' + str(self.position.x) + ',' + str(self.position.y) + ') - ' + self.colour)

class FloodGrid:
    def __init__(self, data):
        self.height = data['board']['height']
        self.width = data['board']['width']
        self.grid = [[FloodNode(Position(x,y)) for x in range(width)] for y in range(height)]
        self.data = data

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

    def get_direction_of_biggest_space(self):
        flood_fill_values = [self.count_yellow(), 
                             self.count_red(),
                             self.count_blue(),
                             self.count_green()]
        biggest_space = flood_fill_values.index(max(flood_fill_values))
        ff_direction = 'left' if biggest_space == 0 else 'right' if biggest_space == 1 else 'up' if biggest_space == 2 else 'down'
        return ff_direction

    def flood_fill_left(self, node, target_colour, replace_colour):
        if (check_for_obstacle(data, node.position)):
            node.colour = 'black'
            self.insert(node)
            print('found an obstacle')
            return
        else:
            self.insert(node)
        if (target_colour == replace_colour):
            return
        if (self.get_node_at(node.position.x, node.position.y).colour != target_colour):
            print('node is not target colour')
            return
        if (not check_for_obstacle(data, get_position_to_left(node.position))):
            westNode = FloodNode(get_position_to_left(node.position), 'yellow')
            self.insert(westNode)
            flood_fill_left(westNode, target_colour, replace_colour)
        return

    def flood_fill_right(self, node, target_colour, replace_colour):
        if (check_for_obstacle(data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            self.insert(node)
        if (target_colour == replace_colour):
            return
        if (self.get_node_at(node.position.x, node.position.y).colour != target_colour):
            return
        if (not check_for_obstacle(data, get_position_to_right(node.position))):
            eastNode = FloodNode(get_position_to_right(node.position), 'red')
            self.insert(eastNode)
            flood_fill_right(eastNode, target_colour, replace_colour)
        return

    def flood_fill_up(self, node, target_colour, replace_colour):
        if (check_for_obstacle(data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            self.insert(node)
        if (target_colour == replace_colour):
            return
        if (self.get_node_at(node.position.x, node.position.y).colour != target_colour):
            return
        if (not check_for_obstacle(data, get_position_above(node.position))):
            northNode = FloodNode(get_position_above(node.position), 'blue')
            self.insert(northNode)
            flood_fill_up(northNode, target_colour, replace_colour)
        return

    def flood_fill_below(self, node, target_colour, replace_colour):
        if (check_for_obstacle(data, node.position)):
            node.colour = 'black'
            self.insert(node)
            return
        else:
            self.insert(node)
        if (target_colour == replace_colour):
            return
        if (self.get_node_at(node.position.x, node.position.y).colour != target_colour):
            return
        if (not check_for_obstacle(data, get_position_below(node.position))):
            southNode = FloodNode(get_position_below(node.position), 'green')
            self.insert(southNode)
            flood_fill_below(southNode, target_colour, replace_colour)
        return
