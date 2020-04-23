from plotting import *
from disk_movement import *
import numpy as np
from celluloid import Camera



# Define constants
N = 2 # Number of disks
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
disks.append([-50,20,1,0,RADIUS])
disks.append([50,0,-1,0,RADIUS])

# Make a numpy array out of the disks array
disks = np.array(disks)

# Setup a plot and initialize camera for animation
fig, ax = plot_setup(X_LIMITS, Y_LIMITS)
camera = Camera(fig)
# Simulate for a number of steps
t = 0
print('Running simulation')
d1 = disks[0]
d2 = disks[1]

res = time_to_next_collision(d1,d2)
if res:
    t1, t2 = res
    dt = min(t1,t2)
    disks = move_disks(disks, dt)
    plot_disks(disks,ax)
    plt.show()
else:
    print('no collision possible')









