

# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import scienceplots

plt.style.use('science')

# read in csv file with pandas and group by file name
df = pd.read_csv('./results/compute_time_vs_f_score_range_of_goals.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time


df = df[df['Compute Time'] > 0.3]
df_grouped = df.groupby('KL Divergence')

# goals = [0.001, 0.002, 0.004, 0.008, 0.01, 0.02,0.04, 0.08, 0.1, 0.2, 0.4, 0.5]
goals = [32,64,128]


cmap = plt.cm.Spectral
norm = plt.Normalize(vmin=np.log(goals[0]), vmax=np.log(goals[-1]))

# create a plot for each file name all in the same figure
fig, ax = plt.subplots()
for name, group in df_grouped:
    kl_div = group['KL Divergence'].iloc[0]
    colour = cmap(norm(np.log(kl_div)))
    ax.scatter(group['Compute Time'], group['F-Score'], marker='x', c=colour, label=name)

ax.legend(title="KL Div. Goal")
# change the x scale to be logarithmic
ax.set_xscale('log')
# Put the legend out of the figure
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper center', borderaxespad=0.)
plt.xlabel('Compute Time (s), Logarithmic Scale')
plt.ylabel('F-Score')
plt.title('F-Score vs Compute Time for IDMT-SMT-Drums Subset')
cmap = plt.get_cmap('hot')
plt.set_cmap(cmap)
plt.show()
