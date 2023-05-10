import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import scienceplots

plt.style.use('science')
    # hex_colours = ['#%02x%02x%02x'
# read in csv file with pandas and group by file name
df = pd.read_csv('./results/parallel_vs_non.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time


df = df[df['Compute Time'] > 0.3]
df_grouped = df.groupby('Num Chunks')

parallel = df_grouped.get_group(6)
non_parallel = df_grouped.get_group(1)

parallel = parallel.groupby('File Name')
non_parallel = non_parallel.groupby('File Name')

parallel_compute_times = []
parallel_real_times = []
parallel_f_scores = []

for name, group in parallel:
        parallel_compute_times.append(np.mean(group['Compute Time']))
        parallel_f_scores.append(np.mean(group['F-Score']))
        parallel_real_times.append(group['Real Time'].iloc[0])

non_parallel_compute_times = []
non_parallel_real_times = []
non_parallel_f_scores = []

for name, group in non_parallel:
        non_parallel_compute_times.append(np.mean(group['Compute Time']))
        non_parallel_f_scores.append(np.mean(group['F-Score']))
        non_parallel_real_times.append(group['Real Time'].iloc[0])


# Plot the results
fig, ax = plt.subplots()
ax.scatter(parallel_real_times, parallel_compute_times, c='r', label='Parallel', s=5)
ax.scatter(non_parallel_real_times, non_parallel_compute_times, c='b', label='Non-Parallel', s=5)

# shade area between y=x and y=0
x = np.linspace(0, 22, 100)
ax.fill_between(x, x, 0, facecolor='grey', alpha=0.5)
ax.legend()
ax.yaxis.set_label_text('Compute Time (s)')
ax.xaxis.set_label_text('Audio File Duration (s)')
ax.set_title('Compute Time vs Audio File Duration for Parallel and Non-Parallel PfNMF')
plt.show()
print("dummy")
