from plotting import *
from disk_movement import *
import numpy as np
import sys

# Define constants
N_list = [1, 2, 3, 4]  # Number of disks
# runs per N
RUNS = 500
# Set radius
RADIUS = 5
# Set box limits
X_LIMITS = [-100, 100]
Y_LIMITS = [-100, 100]
# Set maximum speed in one direction
VELOCITY = 4
# Set maximum time step for side checks to be smooth
T_STEP = 1

# Array for storing return time results
return_times = np.empty((len(N_list), RUNS), dtype=float)

for l, N in enumerate(N_list):
    print('N = {}'.format(N))

    for k in range(RUNS):
        # Create new disks
        disks = np.empty((0, 5), float)  # List of all disks
        for i in range(N):
            # Initialize random positions and check that they are non overlapping
            while True:
                # Generate new positions (they should all be on the left half)
                x = np.random.random() * (X_LIMITS[0] + 2 * RADIUS)
                y = (np.random.random() - 0.5) * (Y_LIMITS[1] - Y_LIMITS[0] - 2 * RADIUS)
                # Check if this position is not overlapping with other
                if (np.sqrt((disks[:, 0] - x) ** 2 + (disks[:, 1] - y) ** 2) > 2 * RADIUS).all() or disks.shape[0] == 0:
                    # Initialize random velocity direction
                    vx = (np.random.random() - 0.5)
                    vy = (np.random.random() - 0.5)
                    v = np.array([vx, vy])
                    # rescale velocity to the required magnitude
                    vx, vy = v * VELOCITY / np.sqrt(np.sum(v ** 2))
                    # Create a disk row and append to list of all disks
                    disks = np.append(disks, [[x, y, vx, vy, RADIUS]], axis=0)
                    break

        # Simulate for a number of steps
        t = 0
        return_t = 0  # return time

        all_disks_returned = False
        still_in_start = True

        # Run the simulation for some time and then check when the disks return
        while still_in_start or not all_disks_returned:
            # Calculate time to next wall hit
            dt_wall, disk_num = time_to_next_wall_collision(disks, X_LIMITS, Y_LIMITS)
            if N > 1:
                dt_disk, disk_coll1, disk_coll2 = time_next_disk_disk_collision(disks)
            else:
                dt_disk = 999999.9
            # Set time step to simulate until next hit or until disk hits wall
            dt = min(dt_wall, T_STEP, dt_disk)

            # Add time step to global animation time
            t += dt
            return_t += dt  # update return time

            # Move disks by time step
            disks = move_disks(disks, dt)
            # If time step was initiated by wall hit -> update velocities according to wall hit
            if dt == dt_wall:
                disks = update_disk_velocities_wall_collision(disks, disk_num, X_LIMITS, Y_LIMITS)
            if dt == dt_disk:
                disks = update_disk_velocities_collision(disks, disk_coll1, disk_coll2)

            # check if all disks returned
            if (disks[:, 0] < -RADIUS).all() and still_in_start is False:
                all_disks_returned = True
            if not (disks[:, 0] < 0).all() and still_in_start:
                still_in_start = False
                return_t = 0  # Reset return time

        return_times[l, k] = return_t
        if return_t < 0:
            sys.exit('ERROR NEGATIVE RETURN TIME')

# reset plots
plt.clf()
# Plot return times mean
plt.title('{0} runs, V = {1:1.2f}, R = {2}'.format(RUNS, VELOCITY, RADIUS))
plt.errorbar(N_list, np.mean(return_times, axis=1), yerr=np.std(return_times, axis=1), fmt='x')
plt.ylabel('Return time in seconds')
plt.xlabel('Number of disks')
plt.ylim(0, np.max(np.mean(return_times, axis=1)) * 1.1)
filename = 'results/returntimes_N{0}_R{1}_V{2}_RUNS{3}'.format(
    N_list[-1], RADIUS, int(VELOCITY), RUNS)
# Save plot and data
plt.savefig(filename + '.png')
np.save(filename + '.csv', return_times, delimiter=',')
plt.show()
