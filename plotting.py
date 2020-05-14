import matplotlib.pyplot as plt
from disk_movement import get_temperature
import numpy as np


def plot_setup_box(xlimits, ylimits):
    """ Sets up a plot for plotting boxes"""
    # Create plots
    fig, ax = plt.subplots()
    # Set plot limits as box
    ax.set_xlim(xlimits)
    ax.set_ylim(ylimits)
    # Hide numbers on axis
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    # Set for a box plot (otherwise circles are stretched)
    ax.set_aspect('equal', 'box')
    return fig, ax


def plot_disks(disks, ax):
    """ Plots all disks within a box model """
    # plot each disk
    circles = []
    for d in disks:
        circle = plt.Circle([d[0], d[1]], d[-1], color='r')
        circles.append(circle)
        ax.add_artist(circle)
    return ax, circles


def plot_setup_distribution(disks):
    """ Sets up a plot for plotting distribution of velocities"""
    # create plots
    fig, ax = plt.subplots()
    # get all velocities from disks array
    velos = np.sqrt(disks[:, 2] ** 2 + disks[:, 3] ** 2)
    # set limits
    ax.set_xlim([0, np.ceil(np.max(velos))])
    ax.set_ylim([0, 1])
    # return setup plots
    return fig, ax


def plot_distribution(disks, ax, bins=20):
    """ Plots the distribution of velocities of all disks"""
    # get absolute velocities of all disks
    velos = np.sqrt(disks[:, 2] ** 2 + disks[:, 3] ** 2)
    ax.set_ylim([0, 1])
    # plot histogram of all velocities
    ax.hist(velos, bins=bins, color='b', density=True)
    # plot true distribution
    ax = plot_maxwell(0, np.max(bins), get_temperature(disks), ax)
    return ax


def plot_maxwell(x_min, x_max, T, ax):
    """ Plots the maxwell distribution."""
    x = np.linspace(x_min, x_max, 100)
    y = x / T * np.exp(-(x ** 2) / (2 * T))
    ax.plot(x, y, c='red')
    return ax
