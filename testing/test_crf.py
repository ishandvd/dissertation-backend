
import matplotlib.pyplot as plt
import csv
import pandas as pd
import colorsys
import numpy as np
import json
import scienceplots
import Levenshtein


# read in csv file with pandas and group by file name
df = pd.read_csv('C:\Cambridge\Monkee\diss\second_crf_test_set_with_predicted_rationales.csv')
# remove zero compute time rows
# File Name,F-Score,KL Divergence,Compute Time


actual_rationales = df['rationales'].tolist()
predicted_rationales = df['predicted_rationales2'].tolist()

# Calculate the Levenshtein distance between each pair of strings
distances = [Levenshtein.distance(actual, predicted) for actual, predicted in zip(actual_rationales, predicted_rationales)]

# Calculate the maximum possible distance for strings of the same length
max_distance = max(len(actual_rationales), len(predicted_rationales))

# Normalize the distances by dividing by the maximum possible distance
normalized_distances = [distance / max_distance for distance in distances]

# Add the normalized distances as a new column in the DataFrame
df['normalized_distance'] = normalized_distances


print("dummy")

def norm_dists(rationales_col, predicted_col):
    zipped_cols = zip(rationales_col, predicted_col)
    return [Levenshtein.distance(str(actual),str(predicted)) / max(len(str(actual)), len(str(predicted))) for actual, predicted in zipped_cols]

fig, ax = plt.subplots(1,2)
ax[0].set_ylabel("Frequency")
ax[1].set_title("Regex-Generated Rationales")
ax[0].set_title("CRF-Generated Rationales")
fig.text(0.5, 0.04, 'Normalised Levenshtein Distance from Human-Annotated Rationales', ha='center',fontsize=14)
fig.suptitle("Weak Supervision Learning Generated Rationales (IMDB Small Dataset)", fontsize=16)
# ax[0].hist(norm_dists(df['rationales'], df['predicted_rationales2']), bins=400)