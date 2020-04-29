import matplotlib.pyplot as plt
import numpy as np


def plot_setup_box(xlimits, ylimits):
    """ Sets up a plot for plotting boxes"""
    # Create plots
    fig, ax = plt.subplots()
    # Set plot limits as box
    ax.set_xlim(xlimits)
    ax.set_ylim(ylimits)
    # Set for a box plot (otherwise circles are stretched)
    ax.set_aspect('equal', 'box')
    # TODO: Hide numbers on axis
    return fig,ax

def plot_disks(disks, ax):
    """ Plots all disks within a box model """
    # plot each disk
    for d in disks:
        circle = plt.Circle([d[0],d[1]], d[-1], color='r')
        ax.add_artist(circle)
    return ax

def plot_setup_distribution(disks):
    """ Sets up a plot for plotting distribution of velocities"""
    # create plots
    fig, ax = plt.subplots()
    # get all velocities from disks array
    velos = np.sqrt(disks[:,2]**2 + disks[:,3]**2)
    # set limits
    ax.set_xlim([0,np.ceil(np.max(velos))])
    #ax.set_ylim([0,np.sqrt(disks.shape[0])])
    # return setup plots
    return fig, ax

def plot_distribution(disks, ax, bins=20):
    """ Plots the distribution of velocities of all disks"""
    # get absolute velocities of all disks
    velos = np.sqrt(disks[:,2]**2 + disks[:,3]**2)
    # plot histogram of all velocities
    ax.hist(velos,bins=bins)
    return ax




