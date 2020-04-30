# HardDisks

This project simulates the movement of two dimensional disks within a box. All disks are 
initialized at random, non-overlapping positions with random velocities. Collisions of disks 
and walls are shown, as well as collisions between different disks. The dynamics of the disks 
should follow real physics of collisions, as you can see in the following animation:

![Dynamics 10 balls](results/dynamics.gif)

## Project structure
All relevant codefiles for the simulation are located here within the root folder of the repository.

* `disk_movement.py` - contains function to calculate next collision times and update velocity vectors
after collisions
* `plotting.py` - all functions used for plotting are bundled here, for later use.
* `animation.py` - animates the movement of the disks either live or stores as GIF. For high
number of disks, the live animation is not running smoothly.
* `returntime.py` - Calculates the average return time for different numbers of disks.
* `distribution.py` - Animates the velocity distribution for all disks as histogram

## Return times

## Velocity distribution

## Live animations
To run the live animations you need to have `TKinter` installed for python on your system.
This can be done by running ``` sudo apt-get install python3-tk``` on Ubuntu.  