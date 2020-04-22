import numpy as np

def time_to_next_wall_collision(disks, xlim, ylim):
    """ Calculates the time until the next disks hits the next wall """
    min_time = 999999999
    disk_num = 0
    # Iterate through disks
    for i in range(disks.shape[0]):
        disk = disks[i]
        # check positive x velocity
        if disk[2] > 0:
            t = (np.abs(xlim[1] - disk[0]) - disk[-1]) / np.abs(disk[2])
            if min_time > t:
                min_time = t
                disk_num = i
        # check negative x velocity
        if disk[2] < 0:
            t = (np.abs(xlim[0] - disk[0]) - disk[-1]) / np.abs(disk[2])
            if min_time > t:
                min_time = t
                disk_num = i
        # check positive y velocity
        if disk[3] > 0:
            t = (np.abs(ylim[1] - disk[1]) - disk[-1]) / np.abs(disk[3])
            if min_time > t:
                min_time = t
                disk_num = i
        if disk[3] < 0:
            t = (np.abs(ylim[0] - disk[1]) - disk[-1]) / np.abs(disk[3])
            if min_time > t:
                min_time = t
                disk_num = i
    # Return minimum time of next wall hit and number of disk to hit wall
    return min_time, disk_num

def update_disk_velocities_wall_collision(disks, disk_num , xlim, ylim):
    """ Updates the velocities for a given disk after a wall collision
        Also checks if the wall is actually hit.
    """
    # Check if given disks hits a wall
    disk = disks[disk_num]
    # Check if disk hits a vertical wall
    if np.abs(disk[0] - xlim[0]) <= disk[-1] or np.abs(disk[0] - xlim[1]) <= disk[-1]:
        # update velocities -> here: reverse x velocity
        disks[disk_num, 2] = -disks[disk_num, 2]
        return disks
    # check if disk hits a horizontal wall
    if np.abs(disk[1] - ylim[0]) <= disk[-1] or np.abs(disk[1] - ylim[1]) <= disk[-1]:
        # update velocity -> here: reverse y velocity
        disks[disk_num, 3] = -disks[disk_num, 3]
        return disks
    # if no wall was hit return false (should result in error)
    # TODO: Maybe add an assertion error to see where error originates from
    print('Warning: NO DISK HAS HIT THE WALL, BUT IT WAS ASSUMED THAT ONE DOES')
    return False









def move_disks(disks, delta_t):
    """ Moves disks by a time step delta_t """
    for i in range(disks.shape[0]):
        # Move disks by their current velocity and delta_t
        disks[i, 0] += disks[i,2] * delta_t
        disks[i, 1] += disks[i, 3] * delta_t
    return disks
