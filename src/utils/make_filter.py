import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

import matplotlib.pyplot as plt
import numpy as np
from settings import FILTER_DIR


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def plot_random_points(height):
    '''
    height -> tuple containing bottom and top boundary
    width -> integer representing width of the segment
    '''
    step = 100
    # split height into segments
    rows = [(h, h + step) for h in range(height[0], height[1], step)]

    dots = []
    time = []
    cmap = get_cmap(len(rows))
    row_shapes = ['o', 'v', '<', '>', '^', '8', 's', 'p', 'P', '*', 'h', '+', 'X', 'D']
    for row_index, row in enumerate(rows):
        marker_style = row_shapes[row_index % len(row_shapes)]
        # number of dots per row
        dots_per_row = 4
        pattern_size = 4
        pattern_values = []
        pattern_time = []

        for i in range(0, pattern_size):
            pattern_values.append(np.random.rand() * (row[1] - row[0]) + row[0])

        pattern_time = np.linspace(0, 0.5, pattern_size)

        t_delta = 0
        rand_color = int(np.random.rand() * len(rows))
        for row in range(int(dots_per_row / pattern_size)):
            for i, value in enumerate(pattern_values):
                plt.plot(pattern_time[i] + t_delta, value, marker_style, markersize=2, color=cmap(rand_color))
                time.append(pattern_time[i] + t_delta)
                dots.append(value)
            t_delta += 0.50
    return time, dots

# Create Figure and Axes instances
fig = plt.figure(frameon=False)
# 500 x 500 pixels
fig.set_size_inches(0.2, 4.8)

# save fig with only spectogram content
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

plt.margins(x=0)
plt.ylim(0, 3000)
plot_random_points((0, 3000))
plt.savefig(FILTER_DIR + 'filter2.png', transparent=True)
