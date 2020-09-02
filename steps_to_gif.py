import imageio
images = []

filenames = ['steps/maze_step{}.jpg'.format(i) for i in range(1, 1826)]

for i in range(len(filenames)):
    if i% 100 == 0:
        print(i)
    images.append(imageio.imread(filenames[i]))
imageio.mimsave('maze_anim.gif', images, duration = 0.05)
