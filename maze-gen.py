import sys
import time
import argparse

# print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

import numpy as np
from PIL import Image
from functions import *
import random

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

    def get_frontiers(self, coords, value=0):
        directions = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0]
        ]

        fs = []

        for d in directions:
            f = (coords[0] + 2 * d[0], coords[1] + 2 * d[1])
            if f[0] in range(self.width) and f[1] in range(self.height) and self.grid[f[1]][f[0]] == value:
                fs.append(f)

        return fs

    def fast_prim(self):
        start = time.time()
        current_location = [np.random.randint(0, self.width), np.random.randint(0, self.height)]

        directions = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0]
        ]

        frontiers = self.get_frontiers(current_location)

        self.grid[current_location[1]][current_location[0]] = 1

        print(self.grid)
        print(frontiers)
        i = 1
        shuffle_count = 1

        while len(frontiers) > 0:
            if i% 1000 == 0:
                print("* Step {}: {} frontiers unexplored".format(i, len(frontiers)))
            i += 1

            # pick a random frontier point
            # if shuffle_count >= np.sqrt(len(frontiers)):
            #     np.random.shuffle(frontiers)
            #     shuffle_count = 1
            idx = np.random.randint(0, len(frontiers))
            next_f = frontiers[idx]
            frontiers = frontiers[:idx] + frontiers[idx + 1:]
            shuffle_count += 1

            # find a random nearest point
            neighbours = self.get_frontiers(next_f, value=1)
            np.random.shuffle(neighbours)
            next_n = neighbours[0]
            next_d = [int((next_f[0] - next_n[0])/2), int((next_f[1] - next_n[1])/2)]

            if self.grid[next_n[1] + next_d[1]][next_n[0] + next_d[0]] == 0:
                # mark frontier, wall in between as 0
                self.grid[next_f[1]][next_f[0]] = 1
                self.grid[next_n[1] + next_d[1]][next_n[0] + next_d[0]] = 1

                for f in self.get_frontiers(next_f):
                    if not(f in frontiers):
                        frontiers.append(f)
        print("* Finished in {} seconds!".format(time.time() - start))

    def growing_tree(self, p):
        start = time.time()

        current_location = [np.random.randint(0, self.width), np.random.randint(0, self.height)]

        directions = [
            [0, -1],
            [0, 1],
            [-1, 0],
            [1, 0]
        ]

        cells = [current_location]

        self.grid[current_location[1]][current_location[0]] = 1

        i = 1

        while len(cells) > 0:
            if i% 1000 == 0:
                print("* Step {}: {} cells with viable borders".format(i, len(cells)))
            i += 1
            # find a random nearest point
            neighbours = self.get_frontiers(current_location)

            # if there's a valid point to go to, pick one at random and go to it
            if len(neighbours) > 0:
                np.random.shuffle(neighbours)
                next_n = neighbours[0]
                next_d = [int((current_location[0] - next_n[0])/2), int((current_location[1] - next_n[1])/2)]

                # set values for cell and passage between them
                self.grid[next_n[1]][next_n[0]] = 1
                self.grid[next_n[1] + next_d[1]][next_n[0] + next_d[0]] = 1

                # add to cells list and update location
                cells.append(next_n)
                current_location = self.pick_next_cell(cells, p)
            else:
                # current location is no longer viable
                cells.remove(current_location)
                # pick a new current_location unless we are done
                if len(cells) > 0:
                    current_location = self.pick_next_cell(cells, p)

        print("* Finished in {} seconds!".format(time.time() - start))

    def growing_tree_with_loops(self, p, l_p):
        self.growing_tree(p)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                current_location = [j, i]

                neighbours = self.get_frontiers(current_location)
                if len(neighbours) == 2 and self.grid[i][j] == 0:
                    if random.random() < l_p:
                        self.grid[i][j] = 1

    def pick_next_cell(self, arr, prob):
        # No point generating random numbers for the edge cases
        if prob == 0:
            return arr[-1]
        elif prob == 1:
            return arr[np.random.randint(0, len(arr))]
        else:
            if np.random.random() > prob:
                return arr[-1]
            else:
                return arr[np.random.randint(0, len(arr))]

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

parser = argparse.ArgumentParser()

parser.add_argument('--height', '-y', type=int)
parser.add_argument('--width', '-x', type=int)
parser.add_argument('--probability', '-p', type=float)
parser.add_argument('--outfile', '-o', type=str)

args = parser.parse_args()

gen = MazeGenerator(args.width, args.height)
# gen.prim()
# gen.grid_to_png('maze.png')
# gen.fast_prim()
# gen.grid_to_png('fast-prim.png')
#
# gen = MazeGenerator(200, 200)
# gen.recursive_backtracking()
# gen.grid_to_png('recursive-backtracking.png')

gen.growing_tree(args.probability)
gen.grid_to_png(args.outfile)
