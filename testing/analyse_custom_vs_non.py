

# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np


# read in csv file with pandas and group by file name
df = pd.read_csv('./results/custom_vs_non.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time

df = df[df['F-Score'] > 0.01]
df_grouped = df.groupby('Custom Training')

# cmap = plt.cm.Spectral

# # create a plot for each file name all in the same figure
# fig, ax = plt.subplots()
# count = 0
# for name, group in df_grouped:
#     label = "Default" if name == 0 else "Custom Trained"
#     colour = 'red' if name == 0 else 'blue'
#     xs = [(name + 1)] * len(group['F-Score'])
#     ax.scatter(xs, group['F-Score'], c=colour, s=2, label=label)
#     mean_avg = group['F-Score'].mean()
#     ax.scatter([(name + 1)], [mean_avg], c=colour, marker='x', s=100)
#     count += 1

# # ax.legend()
# # change the x scale to be logarithmic
# # ax.set_xscale('log')
# # Put the legend out of the figure
# # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper center', borderaxespad=0.)
# # plt.xlabel()
# plt.xticks([0.5,1, 2,4], ["",'Default', 'Custom Trained',""])
# plt.ylabel('F-Score')
# plt.title('F-Score of Custom Trained vs Default Wd Matrix')
# cmap = plt.get_cmap('hot')
# plt.set_cmap(cmap)
# plt.show()



# Generate some example data
default = list(df_grouped.get_group(0)['F-Score'])
custom_training = list(df_grouped.get_group(1)['F-Score'])

# Combine data sets into a list
data = [default, custom_training]

# Create the boxplot
fig, ax = plt.subplots()
ax.boxplot(data)

# Customize the x-axis labels
ax.set_xticklabels(['Default', 'Custom Trained'])

# Add title and labels
ax.set_title('F-Score of Custom Trained vs Default Wd Matrix')
ax.set_ylabel('F-Score')

# Show the plot
plt.show()

# Calculate quartiles for both sets of data
# q1_1, median_1, q3_1 = np.percentile(data1, [25, 50, 75])
# q1_2, median_2, q3_2 = np.percentile(data2, [25, 50, 75])

# # Create grouped box plot
# fig, ax = plt.subplots()
# ax.boxplot([data1, data2], showfliers=False)
# ax.set_xticklabels(['Data 1', 'Data 2'])
# ax.set_ylabel('Values')

# # Add quartile lines for first set of data
# ax.axhline(q1_1, color='r', linestyle='--')
# ax.axhline(median_1, color='g', linestyle='-')
# ax.axhline(q3_1, color='r', linestyle='--')

# # Add quartile lines for second set of data
# ax2 = ax.twinx()
# ax2.axhline(q1_2, color='b', linestyle='--')
# ax2.axhline(median_2, color='m', linestyle='-')
# ax2.axhline(q3_2, color='b', linestyle='--')
# ax2.set_ylim(ax.get_ylim()) # Ensure same y-axis scale as first axis

# plt.show()