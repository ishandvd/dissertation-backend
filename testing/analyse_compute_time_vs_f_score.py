

# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd

# read in csv file with pandas and group by file name
df = pd.read_csv('./results/compute_time_vs_f_score_several_files.csv')
df_grouped = df.groupby('File Name')

# create a plot for each file name all in the same figure
fig, ax = plt.subplots()
for name, group in df_grouped:
    ax.plot(group['Compute Time'], group['F-Score'], marker='x', ms=3, label=name)
ax.legend()
# Put the legend out of the figure
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.xlabel('Compute Time (s)')
plt.ylabel('F-Score')
plt.title('F-Score vs Compute Time for 10 Files')
plt.show()
