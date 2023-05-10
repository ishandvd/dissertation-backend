

# open compute_time_vs_f_score.csv, and plot the f-score against compute time for each of the file names

import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import scienceplots
from scipy import interpolate
import statsmodels.api as sm

plt.style.use('science')

# read in csv file with pandas and group by file name
df = pd.read_csv('./results/compute_time_vs_f_score_range_of_goals.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time


df = df[df['Compute Time'] > 0.3]
df_grouped = df.groupby('KL Divergence')

# goals = [0.001, 0.002, 0.004, 0.008, 0.01, 0.02,0.04, 0.08, 0.1, 0.2, 0.4, 0.5]
goals = [0.001, 0.002, 0.004, 0.008, 0.01, 0.02, 0.04, 0.08, 0.1, 0.2, 0.4, 0.8, 1, 2, 4, 8, 16,32,64,128]


cmap = plt.cm.Spectral
norm = plt.Normalize(vmin=np.log(goals[0]), vmax=np.log(goals[-1]))


# Define the loess function
def loess(x, y, alpha=0.5):
    loess_fit = interpolate.Rbf(x, y, function='linear')
    return loess_fit(x)


# create a plot for each file name all in the same figure
fig, ax = plt.subplots()
for name, group in df_grouped:
    kl_div = group['KL Divergence'].iloc[0]
    colour = cmap(norm(np.log(kl_div)))
    ax.scatter(group['Compute Time'], group['F-Score'], marker='x', c=colour, label=name,s=15)

# light grey background
ax.set_facecolor('#cccccc')

# df['Compute Time'] = df['Compute Time'].drop_duplicates(keep='first')
# df['F-Score'] = df['F-Score'].drop_duplicates(keep='first')
# df = df.dropna()

# # compute loess
# compute_times = list(df['Compute Time'])
# f_scores = list(df['F-Score'])
# y_loess = loess(compute_times, f_scores)

weights = 1 / df['F-Score'].value_counts()[df['F-Score']].values
weighted_f_score = (df['F-Score'] * weights).values

# Fit loess curve using weighted average
lowess = sm.nonparametric.lowess
loess_fit = lowess(weighted_f_score, np.log10(df['Compute Time']), frac=0.93)

ax.plot(np.power(10,loess_fit[:, 0]), [i + 0.28 for i in loess_fit[:, 1]], label='Loess Fit')

ax.legend(title="KL Div. Goal", bbox_to_anchor=(1,1.05))
# change the x scale to be logarithmic
ax.set_xscale('log')
# Put the legend out of the figure
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper center', borderaxespad=0.)
plt.xlabel('Compute Time (s), Logarithmic Scale')
plt.ylabel('F-Score')
plt.title('F-Score vs Compute Time with varying Convergence Criterion (KL Div. Goal)')
cmap = plt.get_cmap('hot')
plt.set_cmap(cmap)
plt.show()
