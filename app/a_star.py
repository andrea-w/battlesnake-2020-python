from app.rb_tree import RedBlackTree

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_valid(self, grid_size):
        if (self.x < 0 || self.x >= grid_size):
            return False
        if (self.y < 0 || self.y >= grid_size):
            return False
        return True

class GridPositionInfo:

    def __init__(self, current, source, goal):
        self.position = current
        self.g = self.get_manhattan_distance(self.position, source.position)
        self.h = self.get_manhattan_distance(self.position, goal.position)
        self.f = self.g + self.h

    def get_manhattan_distance(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

class AStarSearch:

    def __init__(self, grid_size, source, goal):
        self.grid_size = grid_size
        self.goal = goal
        self.open = RedBlackTree()
        self.closed = {}
        first = GridPositionInfo(source, source, goal)
        first.f = 0
        self.open.add(first)

    def iterate_through_open_list():
        while(self.open.count > 0):
            # find node in open list with lowest f value & pop it off open list
            # generate the 8 successors of the node
            successors = generate_successors(node)
            while(successors.len > 0):
                successor = successors.pop()
                if (successor.position == self.goal.position):
                    return successor
                elif (is_cheaper_node_in_open_list(successor)):
                    continue
                elif (is_cheaper_node_in_closed_list(successor)):
                    continue
                else:
                    self.open.add(successor)
            # end nested while
            self.closed[successor.position] = successor
        # end outer while

        # if have reached here, have encountered failure: open list is empty but destination
        # has not been reached
        print('Error: cannot reach ' + self.goal)

    # returns boolean value indicating if a node with the same position as successor
    # already exists in the open R-B tree AND has a lower f value than successor
    def is_cheaper_node_in_open_list(successor):
        print(self.open.contains(successor.position))

    # returns boolean value indicating if a node with the same position as successor
    # already exists in the closed list AND has a lower f value than successor
    def is_cheaper_node_in_closed_list(successor): 
        if (successor.position in self.closed.keys()):
            node = self.closed[successor.position]
            if (node.f < successor.f) return True
        return False      

    def generate_successors(parent):
        successors_list = []
        """
        +---+---+---+
        | 8 | 1 | 2 |
        +---+---+---+
        | 7 | P | 3 |      P = parent
        +---+---+---+
        | 6 | 5 | 4 |
        +---+---+---+
        """
        # first child
        child_1_pos = Position(parent.position.x, parent.position.y+1)
        if (child_1_pos.is_valid(self.grid_size)):
            child_1 = GridPositionInfo(child_1_pos, parent, parent.goal)
            successors_list.append(child_1)
        # second child
        child_2_pos = Position(parent.position.x+1, parent.position.y+1)
        if (child_2_pos.is_valid(self.grid_size)):
            child_2 = GridPositionInfo(child_2_pos, parent, parent.goal)
            successors_list.append(child_2)
        # third child
        child_3_pos = Position(parent.position.x+1, parent.position.y)
        if (child_3_pos.is_valid(self.grid_size)):
            child_3 = GridPositionInfo(child_3_pos, parent, parent.goal)
            successors_list.append(child_3)
        # fourth child
        child_4_pos = Position(parent.position.x+1, parent.position.y-1)
        if (child_4_pos.is_valid(self.grid_size)):
            child_4 = GridPositionInfo(child_4_pos, parent, parent.goal)
            successors_list.append(child_4)
        # fifth child
        child_5_pos = Position(parent.position.x, parent.position.y-1)
        if (child_5_pos.is_valid(self.grid_size)):
            child_5 = GridPositionInfo(child_5_pos, parent, parent.goal)
            successors_list.append(child_5)
        # sixth child
        child_6_pos = Position(parent.position.x-1, parent.position.y-1)
        if (child_6_pos.is_valid(self.grid_size)):
            child_6 = GridPositionInfo(child_6_pos, parent, parent.goal)
            successors_list.append(child_6)
        # seventh child
        child_7_pos = Position(parent.position.x-1, parent.position.y)
        if (child_7_pos.is_valid(self.grid_size)):
            child_7 = GridPositionInfo(child_7_pos, parent, parent.goal)
            successors_list.append(child_7)
        # eighth child
        child_8_pos = Position(parent.position.x-1, parent.position.y+1)
        if (child_8_pos.is_valid(self.grid_size)):
            child_8 = GridPositionInfo(child_8_pos, parent, parent.goal)
            successors_list.append(child_8)
        return successors_list
