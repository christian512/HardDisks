# HardDisks

This project simulates the movement of two dimensional disks within a box. All disks are 
initialized at random, non-overlapping positions with random velocities. Collisions of disks 
and walls are shown, as well as collisions between different disks. The dynamics of the disks 
should follow real physics of collisions, as you can see in the following animation:

![Dynamics 10 disks](results/dynamics.gif)

## Project structure
All relevant files for the simulation are located within the root folder of the repository.
To run the live animations you need to have `TKinter` installed for python on your system.
This can be done by running ``` sudo apt-get install python3-tk``` on Ubuntu. As a writer
for the animations we use `imagemagick`, which should also be installed on your system. 


All python packages needed are listed in the `requirements.txt`. 

### Simulation files
* `animation.py` - animates the movement of the disks either live or exported as GIF. For high
number of disks, the live animation is not running smoothly.
* `returntimes.py` - Calculates the average return time for different numbers of disks.
* `distribution.py` - Animates the velocity distribution for all disks as histogram
* `returntime_plot.py` - Just some small code to put together outputs of `returntimes.py`

### Backend files
* `disk_movement.py` - contains functions to calculate next collision times and update velocity vectors
after collisions
* `plotting.py` - all functions used for plotting are bundled here, for later use.

## Return times
Here we let all disks start in the left half of the box. Then a timer is started as soon one of the 
disks leaves that half of the box. The timer stops, when all disks are back at the initial half of the box.
The time taken between the initial leave and return is called *return time*.
We initialize each of the disks with the same absolute velocity. As you can see from the formulas below (in the Velocity Distribution section)
the temperature is then just given by the square of the velocity. 
Plotting the return times for different numbers of disks and temperatures (velocities), we obtain:

![Return times](results/returntimes.png)

As we can see the return times increase for higher number of disks. However the setting with a single disk has a higher return time, since there are only disk-wall
collision occurring. Thus it takes longer for all (here 1) disk to come back.
Increasing the temperature yields smaller return times as the disks move faster in a high temperature system.

## Velocity distribution
If we initialize all disks with an absolute velocity drawn from a uniform velocity, the distribution 
of velocities will change over time, due to collisions between disks. As the system is closed, the 
temperature of the system will not change. Temperature can be defined via the kinetic energy and 
the equipartition theorem (here in 2D):


![\frac{E_{kin}}{N} = k_B T ](https://render.githubusercontent.com/render/math?math=%5Cfrac%7BE_%7Bkin%7D%7D%7BN%7D%20%3D%20k_B%20T%20)

Using `k_B = 1` and assuming all disks have the same mass `m_i = 1`, results in: 

![T = \frac{\sum v_i^2}{N}](https://render.githubusercontent.com/render/math?math=T%20%3D%20%5Cfrac%7B%5Csum%20v_i%5E2%7D%7BN%7D)

The Maxwell-distribution should model the velocity distribution in equilibrium. Using the same 
simplifications the Maxwell distribution can easily be plotted. 
Plotting the time evolution for an initial uniform velocity distribution, we find that it approaches
the Maxwell distribution for large times. The animation below was done for 500 disks:

![Velocity distribution for 500 disks](results/distribution500.gif)



