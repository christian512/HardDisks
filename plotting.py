import matplotlib.pyplot as plt


def plot_setup(xlimits, ylimits):
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


