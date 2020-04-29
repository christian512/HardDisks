from plotting import *
from disk_movement import *
import numpy as np
from celluloid import Camera
import sys



# Define constants
N = 100 # Number of disks
# Set radius
RADIUS = 5
# Set box limits
X_LIMITS = [-100, 100]
Y_LIMITS = [-100, 100]

# Define the absolute velocity of each disk from a uniform random distribution
VELOCITIES = np.random.uniform(low=0.0,high=10.0,size=N)

# BINS
BINS = 30

# Set maximum time step for histogram plotting (no need for small ones as dynamics of balls is not shown)
T_STEP = 10

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
            vx, vy = v * VELOCITIES[i] / np.sqrt(np.sum(v**2))
            assert np.sqrt(vx**2 + vy**2) - VELOCITIES[i] < 10**(-5), "Velocity does not match!"
            # Create a Disk and append to list of all disks
            disks = np.append(disks, [[x, y, vx, vy, RADIUS]], axis=0)
            break

# Initial plot of distribution
fig, ax = plot_setup_distribution(disks)
plot_distribution(disks, ax, bins=BINS)
plt.savefig('results/initial.png')

# Setup for animation
fig, ax = plot_setup_distribution(disks)
camera = Camera(fig)

# Simulate for a number of steps
t = 0

print('Running simulation')
while t < 200:
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
    print(t)

    # Move disks by time step
    disks = move_disks(disks, dt)
    # If time step was initiated by wall hit -> update velocities according to wall hit
    if dt == dt_wall:
        disks = update_disk_velocities_wall_collision(disks, disk_num, X_LIMITS, Y_LIMITS)
    if dt == dt_disk:
        disks = update_disk_velocities_collision(disks, disk_coll1, disk_coll2)

    # If time is for plotting -> add a new plot to the animation
    if t % T_STEP < 10**(-5):
        ax = plot_distribution(disks, ax, bins=BINS)
        camera.snap()

# Animation
print('Creating animation')
animation = camera.animate(interval=200)
animation.save('results/distribution.mp4', writer='imagemagick')

# plot of final distribution
fig, ax = plot_setup_distribution(disks)
plot_distribution(disks, ax, bins=BINS)
plt.savefig('results/final.png')









