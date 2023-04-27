import matplotlib.pyplot as plt
import json
import numpy as np

with open('./results/varying_windows_512.json', 'r') as fp:
    varying_windows_512 = json.load(fp)

with open('./results/varying_windows_256.json', 'r') as fp:
    varying_windows_256 = json.load(fp)

with open('./results/varying_windows_128.json', 'r') as fp:
    varying_windows_128 = json.load(fp)

windows = [0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01]
windows = [w*1000 for w in windows]


# Clean the data to only include non empty lists and non zero lists
f_scores_512 = [varying_windows_512[key] for key in varying_windows_512.keys() 
            if (len(varying_windows_512[key]) != 0 and varying_windows_512[key] != [0,0,0,0,0,0,0,0,0,0,0])]

f_scores_256 = [varying_windows_256[key] for key in varying_windows_256.keys()
            if (len(varying_windows_256[key]) != 0 and varying_windows_256[key] != [0,0,0,0,0,0,0,0,0,0,0])]

f_scores_128 = [varying_windows_128[key] for key in varying_windows_128.keys()
            if (len(varying_windows_128[key]) != 0 and varying_windows_128[key] != [0,0,0,0,0,0,0,0,0,0,0])]

means_128 = []
means_256 = []
means_512 = []

for i in range(len(windows)):
    mean_128 = np.mean([f_score[i] for f_score in f_scores_128])
    means_128.append(mean_128)
    mean_256 = np.mean([f_score[i] for f_score in f_scores_256])
    means_256.append(mean_256)
    mean_512 = np.mean([f_score[i] for f_score in f_scores_512])
    means_512.append(mean_512)

plt.plot(windows, means_128, label='Hop Size=128')
plt.plot(windows, means_256, label='Hop Size=256')
plt.plot(windows, means_512, label='Hop Size=512')

plt.suptitle('F-scores of Hop Sizes at Various Tolerance Windows, Goal=0.01')
plt.yticks(np.arange(0.25, 1.05, 0.05))
plt.xlabel('Tolerance Window Size (ms)')
plt.ylabel('F-score')
plt.legend()
plt.show()