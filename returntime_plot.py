import matplotlib.pyplot as plt
import numpy as np


# define all files that data should be taken from
files = ['returntimes_N4_R5_V1_RUNS500.csv',
         'returntimes_N4_R5_V2_RUNS500.csv',
         'returntimes_N4_R5_V3_RUNS500.csv',
         'returntimes_N4_R5_V4_RUNS500.csv']
path = 'results/'

# create an array that holds number of disks in rows and velocities in columns : entries are average return times
avg_returntimes = np.zeros([4,len(files)],dtype=float)

#iterate through files and store average return time in array
for i,file in enumerate(files):
    arr = np.genfromtxt(path+file, delimiter=',')
    avg_returntimes[:,i] = np.mean(arr, axis=1)

# plot the results
N_list = np.arange(1,len(files)+1)
temps = np.array([1, 2, 3, 4]) ** 2
colors = ['r', 'g', 'b', 'orange']

for j in range(avg_returntimes.shape[1]):
    label = 'T = {}'.format(temps[j])
    plt.scatter(N_list, avg_returntimes[:,j],c=colors[j],label=label)

plt.title('Return times for different temperatures (averaged over 500 runs)')
plt.ylabel('Average return time')
plt.xlabel('Number of disks')
plt.legend()
plt.tight_layout()
plt.savefig('results/returntimes.png')
plt.show()

