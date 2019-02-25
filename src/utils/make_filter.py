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


def plot_random_points(boundary):
    '''
    boundary -> tuple containing bottom and top boundary
    '''
    step = 200
    # split height into segments
    columns = [(h, h + step) for h in range(boundary[0], boundary[1], step)]

    dots = []
    freq = []
    cmap = get_cmap(len(columns))
    column_shapes = ['o', 'v', '<', '>', '^', '8', 's', 'p', 'P', '*', 'h', '+', 'X', 'D']
    for column_index, column in enumerate(columns):
        marker_style = column_shapes[column_index % len(column_shapes)]
        # number of dots per column
        pattern_size = 10
        pattern_values = []
        pattern_freq = []

        for i in range(0, pattern_size):
            pattern_values.append(np.random.rand())

        pattern_freq = np.random.uniform(column[0], column[1], pattern_size)

        rand_color = int(np.random.rand() * len(columns))
        for i, value in enumerate(pattern_values):
            plt.plot(pattern_freq[i], value, marker_style, markersize=1, color=cmap(rand_color))
            freq.append(pattern_freq[i])
            dots.append(value)
    return freq, dots

# Create Figure and Axes instances
fig = plt.figure(frameon=False)
# 500 x 500 pixels
fig.set_size_inches(0.8, 0.6)

# save fig with only spectogram content
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

plt.margins(x=0)
plt.ylim(0, 1)
plot_random_points((0, 5000))
plt.savefig(os.path.join(FILTER_DIR, 'filter2.png'), transparent=True)
