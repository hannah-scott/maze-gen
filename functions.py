import numpy as np
from PIL import Image
import imageio

def arr_to_png(arr, fname):
    png = []

    for i in range(len(arr)):
        row = []
        for j in range(len(arr[i])):
            # for _ in range(10):
            row.append(arr[i][j] * 255)
        # for _ in range(10):
        png.append(row)

    fft_p = np.array(png)
    fft_p = fft_p.astype(np.uint8)

    # print(fft_p)
    im = Image.fromarray(fft_p)
    im.convert('L')
    im.save(fname)

def get_neighbour_coords(grid, arr):
    try:
        height = len(grid)
        width = len(grid[0])

        x = arr[0]
        y = arr[1]

        out = []
        if y-1 >= 0:
            out.append((x, y-1))

        if x+1 < width:
            out.append((x+1, y))

        if y + 1 < height:
            out.append((x, y+1))

        if x - 1 >= 0:
            out.append((x-1, y))

        return out
    except IndexError:
        return None

def get_element(grid, arr):
    try:
        return grid[arr[1]][arr[0]]
    except IndexError:
        return None

def set_element(grid, arr, value):
    try:
        grid[arr[1]][arr[0]] = value
    except IndexError:
        return None

def scale_png_up(fname, scale):
    im = imageio.imread(fname)

    arr = []
    for row in im:
        r = []
        for el in row:
            for _ in range(scale):
                r.append(el)

        for _ in range(scale):
            arr.append(r)

    imageio.imsave('{}_{}.png'.format(fname[:-4], scale), arr)
