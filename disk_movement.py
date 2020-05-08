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


def update_disk_velocities_wall_collision(disks, disk_num, xlim, ylim):
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
    return disks


def time_to_next_collision(disk1, disk2):
    """ Calculates next collision time between two disks
        For calculation of formulas see handwritten page
    """
    denominator = (disk1[2]-disk2[2])**2+(disk1[3]-disk2[3])**2
    chi = ((disk1[0]-disk2[0])*(disk1[2]-disk2[2])+(disk1[1]-disk2[1])*(disk1[3]-disk2[3]))
    delta = chi**2 - denominator * ((disk1[0]-disk2[0])**2 +
                                    (disk1[1]-disk2[1])**2 - (disk1[-1] + disk2[-1])**2)
    if delta <= 0:
        return False
    t1 = (-chi + np.sqrt(delta)) / denominator
    t2 = (-chi - np.sqrt(delta)) / denominator

    # Return both solutions of the quadratic equation
    return t1, t2


def time_next_disk_disk_collision(disks):
    """ Calculates the time when the next two disks collide"""
    if disks.shape[0] <= 1:
        print('can not calculate disk-disk collision for only one disk!')
        return False
    min_time = 999999999.9
    disk1, disk2 = -1, -1
    # Iterate over all disks
    for i in range(disks.shape[0]):
        for j in range(i, disks.shape[0]):
            # Get time to next collision
            res = time_to_next_collision(disks[i], disks[j])
            # if result was fetched
            if res:
                # unpack the times and update minimum time
                t1, t2 = res
                if t1 < 0 or t2 < 0:
                    continue
                dt = min(t1, t2)
                if dt < min_time:
                    min_time = dt
                    disk1, disk2 = i, j
    if min_time <= 0:
        print('Negative collision time')
    return min_time, disk1, disk2


def update_disk_velocities_collision(disks, disk1, disk2):
    """ Update the disk velocities of two disk that collide """
    # Get velocity vectors
    v1 = np.array([disks[disk1, 2], disks[disk1, 3]])
    v2 = np.array([disks[disk2, 2], disks[disk2, 3]])
    # distance vector
    d1 = np.array([disks[disk1, 0] - disks[disk2, 0], disks[disk1, 1] - disks[disk2, 1]])
    d2 = np.copy(d1)
    d = d1[0]**2 + d1[1]**2
    # get parallel vectors
    v1_para = np.dot(v1, d1) * d1 / d
    v2_para = np.dot(v2, d2) * d2 / d

    # get perpendicular vectors
    v1_perp = v1 - v1_para
    v2_perp = v2 - v2_para

    # Assuming both disks have same weight, update the parallel velocities
    # and transform back to x and y
    disks[disk1, 2] = v2_para[0] + v1_perp[0]
    disks[disk1, 3] = v2_para[1] + v1_perp[1]
    disks[disk2, 2] = v1_para[0] + v2_perp[0]
    disks[disk2, 3] = v1_para[1] + v2_perp[1]
    # Return new disks array
    return disks


def move_disks(disks, delta_t):
    """ Moves disks by a time step delta_t """
    for i in range(disks.shape[0]):
        # Move disks by their current velocity and delta_t
        disks[i, 0] += disks[i, 2] * delta_t
        disks[i, 1] += disks[i, 3] * delta_t
    return disks
