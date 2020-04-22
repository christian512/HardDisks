from plotting import *
from disk_movement import *
import numpy as np
from celluloid import Camera



# Define constants
N = 4 # Number of disks
# Set radius
RADIUS = 5
# Set box limits
X_LIMITS = [-100, 100]
Y_LIMITS = [-100, 100]
# Set maximum speed in one direction
V_MAX = 3

# Set maximum time step (for visualizations to be smooth)
T_STEP = 1

# Seed random number generator for reproducibility


# Create new disks
disks = [] # List of all disks
for _ in range(N):
    # Initialize random positions
    x = (np.random.random() - 0.5) * (X_LIMITS[1] - X_LIMITS[0] - RADIUS)
    y = (np.random.random() - 0.5) * (Y_LIMITS[1] - Y_LIMITS[0] - RADIUS)

    # Initialize random velocities (measured in m/s)
    vx = (np.random.random() - 0.5) * V_MAX * 2
    vy = (np.random.random() - 0.5) * V_MAX * 2

    # Create a Disk and append to list of all disks
    disks.append([x,y,vx,vy,RADIUS])

# Make a numpy array out of the disks array
disks = np.array(disks)

# Setup a plot and initialize camera for animation
fig, ax = plot_setup(X_LIMITS, Y_LIMITS)
camera = Camera(fig)
# Simulate for a number of steps
t = 0
print('Running simulation')
while t < 250:
    # Calculate time to next wall hit
    dt_wall, disk_num = time_to_next_wall_collision(disks, X_LIMITS, Y_LIMITS)
    # Set time step to simulate until next hit or until disk hits wall
    dt = min(dt_wall, T_STEP)
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
    # If time is for plotting -> add a new plot to the animation
    if t % T_STEP < 10**(-5):
        ax = plot_disks(disks, ax)
        camera.snap()

# Animation
# TODO: Animation crashed when simulation time is too long (e.g. 500)
print('Creating animation')
animation = camera.animate(interval=20)
animation.save('anim.mp4', writer='imagemagick')









