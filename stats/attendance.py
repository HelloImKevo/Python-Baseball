#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

from data import games

# Select attendance
attendance = games.loc[(games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year', 'multi3']]
# Column labels
attendance.columns = ['year', 'attendance']

# Convert to numeric
attendance.loc[:, 'attendance'] = pd.to_numeric(attendance.loc[:, 'attendance'])

# Plot DataFrame
attendance.plot(x='year', y='attendance', figsize=(15, 7), kind='bar')

# Axis labels
plt.xlabel('Year')
plt.ylabel('Attendance')

# Mean line
plt.axhline(y=attendance['attendance'].mean(), label='Mean', linestyle='--', color='green')

plt.show()
