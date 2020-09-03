import sys

# print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

import numpy as np
from PIL import Image
from functions import *

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid = np.zeros([self.height, self.width])

    def carve_path_from(self, coords):
        directions = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0]
        ]

        np.random.shuffle(directions)

        for d in directions:
            next_wall = [coords[0] + d[0], coords[1] + d[1]]
            next_cell = [coords[0] + 2 * d[0], coords[1] + 2 * d[1]]
            if next_cell[0] in range(self.width) and next_cell[1] in range(self.height) and self.grid[next_cell[1]][next_cell[0]] == 0:
                self.grid[next_wall[1]][next_wall[0]] = 1
                self.grid[next_cell[1]][next_cell[0]] = 1
                self.carve_path_from(next_cell)

    def recursive_backtracking(self):
        # recursive backtracking algorithm
        # initialize a random starting point
        current_location = [np.random.randint(0, self.width), np.random.randint(0, self.height)]
        self.grid[current_location[1]][current_location[0]] = 1
        self.carve_path_from(current_location)
        # print(self.grid)

    def prim(self):
        wall_list = []
        path_list = []
        # initialize a random starting point
        start_coord = [np.random.randint(0, self.width), np.random.randint(0, self.height)]

        set_element(self.grid, start_coord, 1)
        path_list.append(start_coord)

        for n in get_neighbour_coords(self.grid, start_coord):
            if get_element(self.grid, n) == 0:
                wall_list.append(n)

        i = 0

        # prim's algorithm
        while len(wall_list) > 0 and i < 40000:
            i += 1
            l_wall = wall_list[np.random.randint(0, len(wall_list))]
            next_wall = np.array(l_wall)

            manhattan = lambda x, y: np.abs(x[0] - y[0]) + np.abs(x[1] - y[1])
            nearest_paths = [p for p in path_list if manhattan(p, next_wall) == 1]

            if len(nearest_paths) > 0:
                path_choice = nearest_paths[np.random.randint(0, len(nearest_paths))]
                direction = next_wall - path_choice

                next_cell = next_wall + direction

                # print(next_cell)

                if next_cell[0] in range(self.width) and next_cell[1] in range(self.height):

                    if get_element(self.grid, next_cell) != 1:
                        set_element(self.grid, next_wall, 1)
                        set_element(self.grid, next_cell, 1)
                        path_list.append(next_wall)
                        path_list.append(next_cell)

                        for n in get_neighbour_coords(self.grid, next_cell):
                            if get_element(self.grid, n) == 0:
                                wall_list.append(n)

                wall_list.remove(l_wall)

            if i % 100 == 0:
                print("* {}: {}".format(i, len(wall_list)))

            # arr_to_png(grid, 'steps/maze_step{}.jpg'.format(i))

        print("Process ended in {} steps".format(i))

    def grid_to_png(self, fname):
        # remove top or bottom if all zeros
        if np.array(self.grid[0]).sum() == 0:
            self.grid = self.grid[1:]
        if np.array(self.grid[-1]).sum() == 0:
            self.grid = self.grid[:-1]
        if np.array([x[0] for x in self.grid]).sum() == 0:
            self.grid = [x[1:] for x in self.grid]
        if np.array([x[-1] for x in self.grid]).sum() == 0:
            self.grid = [x[:-1] for x in self.grid]

        # surround, add an entrance and an exit
        extended_grid = np.zeros([len(self.grid) + 2, len(self.grid[0]) + 2])
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                extended_grid[i+1][j+1] = self.grid[i][j]

        possible_starts = [x + 1 for x in range(len(self.grid[0])) if self.grid[0][x] == 1]

        # print(possible_starts)
        start = possible_starts[np.random.randint(0, len(possible_starts))]
        extended_grid[0][start] = 1

        possible_ends = [x + 1 for x in range(len(self.grid[0])) if self.grid[-1][x] == 1]

        # print(possible_ends)
        end = possible_ends[np.random.randint(0, len(possible_ends))]
        extended_grid[-1][end] = 1
        arr_to_png(extended_grid, fname)

gen = MazeGenerator(107,233)
# gen.prim()
# gen.grid_to_png('maze.png')
gen.recursive_backtracking()
gen.grid_to_png('recursive-backtracking.png')
