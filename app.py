import streamlit as st
from mazegen import MazeGenerator
import numpy as np

'''
# Maze generator
'''

algorithm = st.radio(label="Algorithm", options = ["Prim's algorithm", 'Recursive backtracking'])

width = st.select_slider('Width', options=range(10,110,10))
height = st.select_slider('Height', options=range(10,110,10))

maze = MazeGenerator(width,height)

if algorithm == "Prim's algorithm":
    maze.fast_prim()
elif algorithm == 'Recursive backtracking':
    maze.recursive_backtracking()

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


st.image(fft_p)
