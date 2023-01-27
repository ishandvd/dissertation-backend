

# open nmf_results.csv, and plot the f-scores

import matplotlib.pyplot as plt
import csv


with open('nmf_results.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    f_scores = [float(row[1]) for row in reader if float(row[1]) > 0.5]

average = sum(f_scores) / len(f_scores)
standard_deviation = (sum([(x - average) ** 2 for x in f_scores]) / len(f_scores)) ** 0.5

print("Average F-Score: %(average).3f" % {"average": average})
print("Standard Deviation: %(standard_deviation).3f" % {"standard_deviation": standard_deviation})

# Plot a histogram of the f-scores
plt.hist(f_scores, bins=30, color='r', alpha=0.5, range=[0,1])
plt.title(("F-Scores for NMF, Tolerance = 0.1, Avg = %(average).3f, " 
            "SD = %(standard_deviation).3f") % 
            {"average": average, "standard_deviation": standard_deviation},
             fontsize=12)
plt.xlabel("F-Score")
plt.ylabel("Frequency")
plt.show()