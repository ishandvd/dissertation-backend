

# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np

    # hex_colours = ['#%02x%02x%02x'
# read in csv file with pandas and group by file name
df = pd.read_csv('./results/nmf_results_num_chunks.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time

# create subplots with two axes
fig, ax = plt.subplots(3,sharex=True)

ax[0].plot(df['Num Chunks'], df['F-Score'])

ax[1].plot(df['Num Chunks'], df['HDs Total Length'])

ax[2].plot(df['Num Chunks'], df['Compute Time'])

for i in range(3):
    fig.supxlabel('Number of Chunks')
    ax[i].set_xticks([int(i) for i in df['Num Chunks']])



ax[0].set_ylabel('F-Score')
ax[1].set_ylabel('Appended Length of Hd\'s')
ax[2].set_ylabel('Compute Time')
fig.suptitle('Results for Different Number of Chunks on RealDrum01_02#MIX.wav')
plt.show()
