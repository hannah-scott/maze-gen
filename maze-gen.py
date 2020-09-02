import numpy as np
from PIL import Image
from functions import *

# setup
width = 100
height = 100

grid = np.zeros([height, width])

def prim(grid):
    global width, height
    wall_list = []
    path_list = []
    # initialize a random starting point
    start_coord = [np.random.randint(0, width), np.random.randint(0, height)]

    set_element(grid, start_coord, 1)
    path_list.append(start_coord)

    for n in get_neighbour_coords(grid, start_coord):
        if get_element(grid, n) == 0:
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

            if next_cell[0] in range(width) and next_cell[1] in range(height):

                if get_element(grid, next_cell) != 1:
                    set_element(grid, next_wall, 1)
                    set_element(grid, next_cell, 1)
                    path_list.append(next_wall)
                    path_list.append(next_cell)

                    for n in get_neighbour_coords(grid, next_cell):
                        if get_element(grid, n) == 0:
                            wall_list.append(n)

            wall_list.remove(l_wall)

        if i % 100 == 0:
            print("* {}: {}".format(i, len(wall_list)))

        # arr_to_png(grid, 'steps/maze_step{}.jpg'.format(i))

    print("Process ended in {} steps".format(i))

    # remove top or bottom if all zeros
    if np.array(grid[0]).sum() == 0:
        grid = grid[1:]
    if np.array(grid[-1]).sum() == 0:
        grid = grid[:-1]
    if np.array([x[0] for x in grid]).sum() == 0:
        grid = [x[1:] for x in grid]
    if np.array([x[-1] for x in grid]).sum() == 0:
        grid = [x[:-1] for x in grid]

    # surround, add an entrance and an exit
    extended_grid = np.zeros([len(grid) + 2, len(grid[0]) + 2])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            extended_grid[i+1][j+1] = grid[i][j]

    possible_starts = [x + 1 for x in range(len(grid[0])) if grid[0][x] == 1]

    # print(possible_starts)
    start = possible_starts[np.random.randint(0, len(possible_starts))]
    extended_grid[0][start] = 1

    possible_ends = [x + 1 for x in range(len(grid[0])) if grid[-1][x] == 1]

    # print(possible_ends)
    end = possible_ends[np.random.randint(0, len(possible_ends))]
    extended_grid[-1][end] = 1

    # print(extended_grid)

    arr_to_png(extended_grid, 'maze.png')

prim(grid)
