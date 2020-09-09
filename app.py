import streamlit as st
from mazegen import MazeGenerator
from mazesolve import Maze
import numpy as np

'''
# Maze generator
'''

algorithm = st.radio(label="Algorithm", options = ["Prim's algorithm", 'Recursive backtracking', 'Growing tree'])

width = st.select_slider('Width', options=range(10,110,10))
height = st.select_slider('Height', options=range(10,110,10))

if algorithm == 'Growing tree':
    prob = st.slider('p', min_value = 0.0, max_value = 1.0, step=0.1)

maze = MazeGenerator(width,height)

if algorithm == "Prim's algorithm":
    maze.fast_prim()
elif algorithm == 'Recursive backtracking':
    maze.recursive_backtracking()
elif algorithm == 'Growing tree':
    maze.growing_tree(prob)

maze.grid = maze.extended_grid()

png = []

for i in range(len(maze.grid)):
    row = []
    for j in range(len(maze.grid[i])):
        for _ in range(10):
            row.append(maze.grid[i][j] * 255)
    for _ in range(10):
        png.append(row)

fft_p = np.array(png)
fft_p = fft_p.astype(np.uint8)

png = np.array(png)
png = png.astype(np.uint8)

if st.checkbox(label="Solve?"):
    maze = Maze(maze.grid)
    maze.dfs()
    st.image(maze.arr_to_png())
else:
    st.image(fft_p)
