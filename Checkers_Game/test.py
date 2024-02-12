import numpy as np

day = []

for i in range(0, 24):
    time_slot = [i, i + 1]
    day.append(time_slot)

print(day)
