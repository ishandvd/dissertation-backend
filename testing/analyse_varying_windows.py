import matplotlib.pyplot as plt
import json
import numpy as np

with open('./results/varying_windows_256.json', 'r') as fp:
    varying_windows = json.load(fp)

windows = [0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01]
windows = [w*1000 for w in windows]


# Clean the data to only include non empty lists and non zero lists
f_scores = [varying_windows[key] for key in varying_windows.keys() 
            if (len(varying_windows[key]) != 0 and varying_windows[key] != [0,0,0,0,0,0,0,0,0,0,0])]


colours = np.linspace(0, 1, len(f_scores))


for i in range(len(windows)):
    window_xs = [windows[i]] * len(f_scores)
    window_ys = [f_score[i] for f_score in f_scores]
    colour = colours[i]
    plt.scatter(window_xs, window_ys, s=3, cmap='viridis')
    average = np.mean(window_ys)
    plt.scatter([windows[i]], [average], c=colour, cmap='viridis', s=100, marker='x')

plt.suptitle('F-scores at Varying Window Sizes, Hop Size=256, Goal=0.01')

# x axis should have ticks for each window size
plt.xticks(windows)
# y axis should have ticks every 0.05 interval between 0 and 1
plt.yticks(np.arange(0, 1, 0.05))
plt.xlabel('Window size (ms)')
plt.ylabel('F-score')
plt.show()
