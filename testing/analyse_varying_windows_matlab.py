import matplotlib.pyplot as plt
import json
import numpy as np
import scienceplots
import pandas as pd

plt.style.use('science')
df = pd.read_csv('./results/matlab_results.csv')
df['F-Scores-List'] = df['F-Scores'].apply(lambda x: json.loads(x))
f_scores_baseline = [f_score for f_score in list(df['F-Scores-List']) if len(f_score) > 0 and f_score[0] > 0]

windows = [0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01]
windows = [w*1000 for w in windows]

with open('./results/varying_windows_512.json', 'r') as fp:
    varying_windows = json.load(fp)

f_scores_pfnmf = [varying_windows[key] for key in varying_windows.keys() 
            if (len(varying_windows[key]) != 0 and varying_windows[key] != [0,0,0,0,0,0,0,0,0,0,0])]




# colours = np.linspace(0, 1, len(f_scores))
windows_x_axis = []
f_avg_baseline = []
f_avg_pfnmf = []
std_baseline = []
std_pfnmf = []

for i in range(len(windows)):
    window_xs = [windows[i]] * len(f_scores_baseline)
    window_ys = [f_score[i] for f_score in f_scores_baseline]
    # plt.scatter(window_xs, window_ys, s=3, cmap='viridis')
    average = np.mean(window_ys)
    windows_x_axis.append(windows[i])
    f_avg_baseline.append(average)
    std_baseline.append(np.std(window_ys))

plt.plot(windows_x_axis, f_avg_baseline, c='red', label='Baseline', marker='o', markersize=3)


for i in range(len(windows)):
    window_xs = [windows[i]] * len(f_scores_pfnmf)
    window_ys = [f_score[i] for f_score in f_scores_pfnmf]
    # plt.scatter(window_xs, window_ys, s=3, cmap='viridis')
    average = np.mean(window_ys)
    f_avg_pfnmf.append(average)
    std_pfnmf.append(np.std(window_ys))

plt.plot(windows_x_axis, f_avg_pfnmf, c='blue', label='My Implementation', marker='o', markersize=3)

plt.suptitle('F-Score at Varying Window Sizes')
plt.legend()

# x axis should have ticks for each window size
plt.xticks(windows)
# y axis should have ticks every 0.05 interval between 0 and 1
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xlabel('Window size (ms)')
plt.ylabel('F-score')

# ci = [i * 1.5 / np.sqrt(len(std_baseline)) for i in std_baseline]
# plt.fill_between(windows_x_axis, (np.array(f_avg_baseline)-np.array(ci)), (np.array(f_avg_baseline)+np.array(ci)), color='r', alpha=.1)

plt.show()
