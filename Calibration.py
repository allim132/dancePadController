# compute_stats.py

import numpy as np
import csv

data = []

with open("sensor_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header

    for row in reader:
        values = list(map(float, row[1:]))  # skip time column
        data.append(values)

data = np.array(data)

means = np.mean(data, axis=0)
stds = np.std(data, axis=0)

print("Means:", means)
print("Stds:", stds)