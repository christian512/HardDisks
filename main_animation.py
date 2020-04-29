from plotting import *
from disk_movement import *
import numpy as np
from celluloid import Camera



# Define constants
N = 10 # Number of disks
# Set radius
RADIUS = 5
# Set box limits
X_LIMITS = [-100, 100]
Y_LIMITS = [-100, 100]
# Set maximum speed in one direction
VELOCITY = 2

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
            vx, vy = v * VELOCITY / np.sqrt(np.sum(v ** 2))
            # Create a Disk and append to list of all disks
            disks = np.append(disks, [[x, y, vx, vy, RADIUS]], axis=0)
            break

# Setup a plot and initialize camera for animation
fig, ax = plot_setup_box(X_LIMITS, Y_LIMITS)
camera = Camera(fig)

# Simulate for a number of steps
t = 0

print('Running simulation')
while t < 250:
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
        ax, _ = plot_disks(disks, ax)
        camera.snap()

# Animation
# TODO: Animation crashed when simulation time is too long (e.g. 500)
print('Creating animation')
animation = camera.animate(interval=20)
animation.save('results/dynamics.gif', writer='imagemagick')









