# -*- coding: utf-8 -*-
"""Helperfunctions for plotting concerns.

Created on Fri Mar  5 12:03:49 2021

@author: 49162
"""

from matplotlib import pyplot as plt
from pylab import cm


def plot_cube_of_success(table, title=''):
    """Visualize chances of success with three dimensional matplotlib plot.

    Parameters
    ----------
    table : pandas.DataFrame
        Contain results to display. At least four columns are expected. First
        theree columns are expected to hold all possible random events by row.
        the fourth column is used to generate the colormap for all dots.
    title : str, optional
        Title to display for the plot.
        Default is ''.

    Returns
    -------
    None.

    """
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
