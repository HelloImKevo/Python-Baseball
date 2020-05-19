#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

from data import games

# Select all plays
plays = games[games['type'] == 'play']

# Select all strike outs
strike_outs = plays[plays['event'].str.contains('K')]
# Group by year and game
strike_outs = strike_outs.groupby(['year', 'game_id']).size()
# Convert GroupBy object to a DataFrame
strike_outs = strike_outs.reset_index(name='strike_outs')
# Apply an operation to multiple columns (converts two selected columns values to numeric)
strike_outs = strike_outs.loc[:, ['year', 'strike_outs']].apply(pd.to_numeric)

# Change plot formatting to use a scatter plot
strike_outs.plot(y='strike_outs', x='year', kind='scatter').legend(['Strike Outs'])

plt.show()
