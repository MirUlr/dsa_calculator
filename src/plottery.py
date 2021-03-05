# -*- coding: utf-8 -*-
"""Helperfunctions for plotting concerns.

Created on Fri Mar  5 12:03:49 2021

@author: 49162
"""

from matplotlib import pyplot as plt
from pylab import cm


def plot_cube_of_success(table, title):
    header = list(table.columns)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
        
    x = table[header[0]]
    y = table[header[1]]
    z = table[header[2]]
    q = table[header[3]]

    colors = cm.Spectral(q / max(q))

    ax.set_xlabel(header[0])
    ax.set_ylabel(header[1])
    ax.set_zlabel(header[2])
    ax.set_title(title)

    ax.scatter(x, y, z, c=colors, s=20, alpha=.5)
    plt.show()
