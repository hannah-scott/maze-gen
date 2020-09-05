import imageio
import numpy as np
from PIL import Image
import time
from functions import *

# get maze from png into array
im = imageio.imread('fast-prim.png')
im = im / 255

class Maze:
    def __init__(self, im):
        self.height = im.shape[0]
        self.width = im.shape[1]
        self.maze = im

        self.best_path = []

        self.start = [[x for x in range(self.width) if self.maze[0][x] == 1][0], 0]
        self.end = [[x for x in range(self.width) if self.maze[-1][x] == 1][0], self.height - 1]

    def values(self):
        return self.maze, (self.height, self.width), self.start, self.end

    def get_ones(self, loc):
        try:
            out = []
            if loc[1] - 1 >= 0:
                if self.maze[loc[1] - 1][loc[0]] == 1:
                    out.append([loc[0], loc[1] - 1])
            if loc[1] + 1 < self.height:
                if self.maze[loc[1] + 1][loc[0]] == 1:
                    out.append([loc[0], loc[1] + 1])
            if loc[0] - 1 >= 0:
                if self.maze[loc[1]][loc[0] - 1] == 1:
                    out.append([loc[0] - 1, loc[1]])
            if loc[0] + 1 < self.width:
                if self.maze[loc[1]][loc[0] + 1] == 1:
                    out.append([loc[0] + 1, loc[1]])
            return out
        except:
            return None

    def dfs(self):
        print("Depth first search")
        start = time.time()
        # depth-first solve
        current_location = self.start


        branching_points = []
        branch_stack = self.get_ones(current_location)
        steps = 2

        # while you're not at the end
        while current_location != self.end:
            # print(self.maze)
            # say you've already been here
            self.maze[current_location[1]][current_location[0]] = 2
            steps += 1
            # print(self.best_path)
            self.best_path.append(current_location)
            # print(current_location)

            ones = self.get_ones(current_location)
            # check if you're in a dead-end
            if ones == None or len(ones) == 0:

                if branching_points[-1] == current_location:
                    branching_points = branching_points[:-1]
                    current_location = branching_points[-1]
                else:
                    current_location = branching_points[-1]

                # trim best path to last branching location
                self.best_path = self.best_path[:self.best_path.index(current_location)]

            # if not, check if you're at a junction
            elif len(ones) > 1:
                # add all directions to the list of branch points, and pick one
                branching_points.append(current_location)

                # branch_stack.append(current_location)
                for b in ones:
                    branch_stack.append(b)

                # go to the next candidate branch
                current_location = branch_stack[-1]
                branch_stack = branch_stack[:-1]
            else:
                 # keep moving
                 current_location = ones[0]
        self.maze[current_location[1]][current_location[0]] = 2
        self.best_path.append(self.end)
        print("Solved! {}s".format(time.time() - start))

        for i in range(len(self.best_path)):
            self.maze[self.best_path[i][1]][self.best_path[i][0]] = - (i + 1)/len(self.best_path)

        return self.maze

    def arr_to_png(self, fname):
        png = []

        for i in range(len(self.maze)):
            row = []
            for j in range(len(self.maze[i])):
                # for _ in range(10):
                if self.maze[i][j] >= 0:
                    row.append([self.maze[i][j] * 255] * 3)
                else:
                    color = np.array([85, 205, 252]) * (-1 * self.maze[i][j]) + np.array([247, 168, 184]) * (1 + self.maze[i][j])
                    color = np.array(color, dtype=int)
                    row.append(color)

            # for _ in range(10):
            # print(row)
            png.append(row)

        fft_p = np.array(png)
        fft_p = fft_p.astype(np.uint8)

        # print(fft_p)
        im = Image.fromarray(fft_p)
        im.convert('RGB')
        im.save(fname)

maze = Maze(im)
maze.dfs()
maze.arr_to_png('solved.png')

scale_png_up('solved.png', 10)
