from copy import deepcopy
from collections import deque
import os

class Node:
    def __init__(self, parent, grid):
        self.parent = parent
        self.grid = grid
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def goaltest(self, grid):
        goal1 = [[0, 0, 1, 2],
                 [3, 4, 5, 6],
                 [7, 8, 9, 10],
                 [11, 12, 13, 14]]

        goal2 = [[1, 2, 3, 4], 
                 [5, 6, 7, 8],
                 [9, 10, 11, 12],
                 [13, 14, 0, 0]]

        if(grid == goal1 or grid == goal2):
            return True
        else:
            return False

    def expand(self, node, frontier):
        print("> Node expansion started, please wait...", "\n")
        first_0 = [None, None]      # [i, j]
        second_0 = [None, None]     # [i, j]

        found_first = False

        #find all blank spaces
        for i in range(4):
            for j in range(4):
                if node.grid[i][j] == 0:
                    if not found_first:
                        first_0 = [i, j]
                        found_first = True
                    else:
                        second_0 = [i, j]

        # perform all possible move
        self.move_left(node, first_0)
        self.move_left(node, second_0)
        self.move_right(node, first_0)
        self.move_right(node, second_0)
        self.move_up(node, first_0)
        self.move_up(node, second_0)
        self.move_down(node, first_0)
        self.move_down(node, second_0)

        # check frontier
        # due to deque mutation error -which I have no idea what it is- frontier is being casted to list
        if not list(frontier):
             for x in node.children:
                frontier.append(x)
        else:
            for x in list(frontier):
                for y in node.children:
                    if y.grid != x.grid:
                        frontier.append(y)
                    # print("frontier incremented: ", len(frontier))

    def move_left(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if j == 0 or node.grid[i][j-1] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i][j-1] = child_grid[i][j-1], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def move_right(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if j == 3 or node.grid[i][j+1] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i][j+1] = child_grid[i][j+1], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)
    
    def move_up(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if i == 0 or node.grid[i-1][j] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i-1][j] = child_grid[i-1][j], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)
    
    def move_down(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if i == 3 or node.grid[i+1][j] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i+1][j] = child_grid[i+1][j], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def bfs(self, frontier, explored, initial_grid):
        while frontier:
            node = deque.popleft(frontier)
            print("> Goal testing...", "\n")
            if(self.goaltest(node.grid)):
                # os.system('cls')
                self.print_answer(initial_grid, node)
                break
            elif node.grid not in explored:
                print("> Not the answer, adding to explored...", "\n")
                explored.append(node.grid)
                self.expand(node, frontier)
            print("> Node expansion completed...", "\n")
            # print("In process frontier: ", len(frontier))
            # print("In process explored: ", len(explored), "\n")
    
    def print_answer(self, initial_grid, node):
        print("Found an answer!", "\n")
        print("Steps: ")
        while node.parent:
            print(node.grid)
            print("==============================================================")
            node = node.parent
        print(initial_grid)
        print("==============================================================", "\n")


def read_input_file(filename, grid):
    numbers = ""
    numbers_counter = 0

    f = open(filename, "r")
    numbers = f.readline().split(" ")
    f.close()

    for i in range(4):
        for j in range(4):
            grid[i][j] = int(numbers[numbers_counter])
            numbers_counter += 1
    
    return grid


grid = [[None for _ in range(4)] for _ in range(4)]
grid = read_input_file("input.txt", grid)

initial = Node(None, grid)

frontier = deque()
frontier.append(initial)
explored = []

initial.bfs(frontier, explored, grid)

print("frontier: ", len(frontier))
print("explored: ", len(explored))