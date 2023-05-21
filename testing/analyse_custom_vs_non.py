
import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import json
import scienceplots


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

plt.style.use('science')

def split_df(dataframe):
    wave = np.mean(dataframe[dataframe['File Name'].str.contains('Wave')]['F-Score'])
    techno = np.mean(dataframe[dataframe['File Name'].str.contains('Techno')]['F-Score'])
    real = np.mean(dataframe[dataframe['File Name'].str.contains('Real')]['F-Score'])
    all = np.mean(dataframe['F-Score'])
    return [np.round(wave,2), np.round(techno,2), np.round(real,2), np.round(all,2)]

# Generate some example data
default = df_grouped.get_group(0)
custom_training = df_grouped.get_group(1)

df_matlab = pd.read_csv('./results/matlab_results.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time

df_matlab = df_matlab[df_matlab['Compute Time'] > 0.3]
df_matlab['F-Score'] = df_matlab['F-Scores'].apply(lambda x: json.loads(x)[2])

# matlab = list(df_matlab['F-Scores'])
# matlab = [json.loads(x)[2] for x in matlab]

algorithm = ("Baseline PfNMF", "PfNMF, Custom Dict.", "Constant Dict.")
category_means = {
    'Techno Drums': (split_df(df_matlab)[1], split_df(custom_training)[1], split_df(default)[1]),
    'Wave Drums': (split_df(df_matlab)[0], split_df(custom_training)[0], split_df(default)[0]),
    'Real Drums': (split_df(df_matlab)[2], split_df(custom_training)[2], split_df(default)[2]),
    'All Drums': (split_df(df_matlab)[3], split_df(custom_training)[3], split_df(default)[3])
}


x = np.arange(len(algorithm))  # the label locations
width = 0.20  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in category_means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('F-score')
ax.set_title('F-Score by Category and Algorithm')
ax.set_xticks(x + width, algorithm)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0.5, 1)

plt.show()
# # Combine data sets into a list
# data = [np.mean(matlab), np.mean(default), np.mean(custom_training)]

# # Create the boxplot
# fig, ax = plt.subplots()
# ax.bar(['Baseline', 'Default', 'Custom Trained'], data)

# # Customize the x-axis labels
# # ax.set_xticklabels(['Baseline', 'Default', 'Custom Trained'])

# # Add title and labels
# ax.set_yticks([0.7, 0.8, 0.9, 1])
# ax.set_title('F-Score of Custom Trained vs Default $W_D$ Matrix')
# ax.set_ylabel('F-Score')

# Show the plot
plt.show()
