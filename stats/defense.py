#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

from frames import games, info, events

# Import existing DataFrames: DER = Defensive Efficiency Ratio (metric to gauge team defense)
# Use query to select all rows with specific type
plays = games.query("type == 'play' & event != 'NP'")
# Adjust the column labels
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

# There are some spots in the event data where there are consecutive rows that represent
# the same at bat. To calculate plate appearances, which is a factor of DER, these need
# to be removed.
# Select all rows that do not match a consecutive row in the player column
# Refine the columns
pa = plays.loc[plays['player'].shift() != plays['player'], ['year', 'game_id', 'inning', 'team', 'player']]
# Group the Plate Appearances
pa = pa.groupby(['year', 'game_id', 'team']).size().reset_index(name='PA')

# Reshape the data by the type of event that happened at each plate appearance.
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
# Unstack the DataFrame
events = events.unstack().fillna(0).reset_index()
events.columns = events.columns.droplevel()
events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE', 'SO']
# Remove the label of the index
events = events.rename_axis(None, axis='columns')

# Merge Plate Appearances
events_plus_pa = pd.merge(events, pa, how='outer', left_on=['year', 'game_id', 'team'], right_on=['year', 'game_id', 'team'])
defense = pd.merge(events_plus_pa, info)
defense.loc[:, 'DER'] = 1 - ((defense['H'] + defense['ROE']) / (defense['PA'] - defense['BB'] - defense['SO'] - defense['HBP'] - defense['HR']))
defense.loc[:, 'year'] = pd.to_numeric(defense['year'])

# Calculate DER (Defensive Efficiency Ratio)
# Equation: 1 - ((H + ROE) / (PA - BB - SO - HBP - HR))
der = defense.loc[defense['year'] >= 1978, ['year', 'defense', 'DER']]
# Reshape with pivot
der = der.pivot(index='year', columns='defense', values='DER')
# Plot formatting: xticks
der.plot(x_compat=True, xticks=range(1978, 2018, 4), rot=45)

plt.show()
