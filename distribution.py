from plotting import *
from disk_movement import *
import numpy as np
import matplotlib.animation as animation
import sys


np.random.seed(42)
# Define constants
N = 500 # Number of disks
# Set radius
RADIUS = 1
# Set box limits
X_LIMITS = [-100, 100]
Y_LIMITS = [-100, 100]
# Set maximum speed in one direction
VELOCITIES = np.random.uniform(low=0.0, high=2.0, size=N)
# bins for histogram
BINS=np.linspace(0,3.5,40)


# Set maximum time step (for visualizations to be smooth)
T_STEP = 1

# Create new disks
disks = np.empty((0,5),float) # List of all disks
print('Placing disks')
for i in range(N):
    # Initialize random positions and check that they are non overlapping
    while True:
        # Generate new positions
        x = (np.random.random() - 0.5) * (X_LIMITS[1] - X_LIMITS[0] - 2 * RADIUS)
        y = (np.random.random() - 0.5) * (Y_LIMITS[1] - Y_LIMITS[0] - 2 * RADIUS)
        # Check if this position is not overlapping with other
        if (np.sqrt((disks[:,0]-x)**2 + (disks[:,1]-y)**2) > 2 * RADIUS).all() or disks.shape[0] == 0:
            # Initialize random velocities (measured in m/s)
            v = np.random.rand(2) - 0.5
            # Rescale the velocity to the absolute value from the already sampled velocities
            vx, vy = v * VELOCITIES[i] / np.sqrt(np.sum(v ** 2))
            # Create a Disk and append to list of all disks
            disks = np.append(disks, [[x, y, vx, vy, RADIUS]], axis=0)
            break

# setup plotting environment
fig, dist_ax = plot_setup_distribution(disks)
# plot circles
dist_ax = plot_distribution(disks, dist_ax, bins=BINS)


# Simulate for a number of steps
t = 0


def update_data(self):
    global t, circles, disks, fig, T_STEP, X_LIMITS, Y_LIMITS, dist_ax
    while True:
        # Calculate time to next wall hit
        dt_wall, disk_num = time_to_next_wall_collision(disks, X_LIMITS, Y_LIMITS)
        dt_disk, disk_coll1, disk_coll2 = time_next_disk_disk_collision(disks)
        # Set time step to simulate until next hit or until disk hits wall
        dt = min(dt_wall, T_STEP, dt_disk)

        # Get back to animation timing schedule if t is off
        if t % T_STEP > 10**(-5):
            dt = min(dt, T_STEP - (t % T_STEP))
        # Add time step to global animation time
        t += dt

        # Move disks by time step
        disks = move_disks(disks, dt)
        # If time step was initiated by wall hit -> update velocities according to wall hit
        if dt == dt_wall:
            disks = update_disk_velocities_wall_collision(disks, disk_num, X_LIMITS, Y_LIMITS)
        if dt == dt_disk:
            disks = update_disk_velocities_collision(disks, disk_coll1, disk_coll2)

        # If time is for plotting -> add a new plot to the animation
        if t % T_STEP < 10**(-5):
            print(t)
            # update disk position
            dist_ax.cla()
            dist_ax = plot_distribution(disks, dist_ax, bins=BINS)
            dist_ax.set_title('t = {}'.format(t))
            # return from while loop
            return disks

print('Running simulation')
simulation = animation.FuncAnimation(fig, update_data, interval=200, frames=5)
simulation.save('results/distribution.gif', writer='imagemagick')



