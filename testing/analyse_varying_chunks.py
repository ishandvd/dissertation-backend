# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import sys
import soundfile as sf

sys.path.append("./utils")
from xml_interface import *

audio_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/audio/"
annotation_folder = r"C:/Cambridge/3rd Year/dissertation/IDMT-SMT-DRUMS-V2/annotation_xml/"

def get_real_time(filename):
    (_,_,_, mix) = training_files_and_mix(annotation_folder + filename)
    (x, fs) = sf.read(audio_folder + mix)
    return len(x)/fs


df = pd.read_csv('./results/varying_chunks_with_overlap_goal_0.04.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time

df = df[df['F-Score'] > 0.01]
df['Real Time'] = df['File Name'].apply(get_real_time)
df_grouped = df.groupby('Num Chunks')

one_chunk = list(df_grouped.get_group(1)['F-Score'])
six_chunks = list(df_grouped.get_group(6)['F-Score'])

# Combine data sets into a list
data = [one_chunk, six_chunks]

# Create the boxplot
fig, ax = plt.subplots()
# ax.boxplot(data)

# # Customize the x-axis labels
# ax.set_xticklabels(['Unparallelized', 'Parallelized'])

# parallelization_mean = df_grouped.get_group(6)['F-Score'].mean()
# no_parallelization_mean = df_grouped.get_group(1)['F-Score'].mean()
# # Add title and labels
# ax.set_title(f'F-Score With (mean={parallelization_mean.round(3)}) and Without (mean={no_parallelization_mean.round(3)}) Parallelization')
# ax.set_ylabel('F-Score')
# ax.set_yticks(np.arange(0.45, 1.05, 0.05))
# # Show the plot
# plt.show()
print("done")



plt.scatter(df_grouped.get_group(6)['Real Time'], df_grouped.get_group(6)['Compute Time'], label='Parallelized', marker='x', s=20)
plt.scatter(df_grouped.get_group(1)['Real Time'], df_grouped.get_group(1)['Compute Time'], label='Unparallelized', marker='x', s=20)
plt.xlabel('Recording Duration')
plt.ylabel('Compute Time')
plt.title("Compute Time against Recording Duration with and without Parallelization")
x = np.arange(0,30,0.1)
y1 = 0 * x
y2 = x
ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green',alpha=0.2, interpolate=True, label='Compute Time < Recording Duration')
plt.legend()
plt.show()
print("done")
