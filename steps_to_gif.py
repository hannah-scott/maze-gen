import imageio
from functions import *

images = []

filenames = ['frames/grid_{}.png'.format(i) for i in range(1, 400)]

for i in range(len(filenames)):
    try:
        if i% 100 == 0:
            print(i)
        images.append(imageio.imread(filenames[i]))
    except:
        print("{}: missing".format(i))
imageio.mimsave('maze_anim.gif', images, duration = 0.005)
