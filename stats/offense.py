#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

from data import games

# Select all plays
plays: pd.DataFrame = games[games['type'] == 'play']
# Label specific columns (to make it easier to access)
plays.columns = ['type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year']

# Select only hits
# Question to answer: "What is the distribution of hits across innings?"
# We need: Hits, singles, doubles, triples and home runs
hits: pd.DataFrame = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]
# Convert the inning column from strings to numbers
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# Define our replacement dictionary for the hit types
replacements: dict = {
  r'^S(.*)': 'single',
  r'^D(.*)': 'double',
  r'^T(.*)': 'triple',
  r'^HR(.*)': 'hr'
}

# Replace the hits with out new dictionary
hit_type: pd.Series = hits['event'].replace(replacements, regex=True)
# Add a new column with the hit type
hits = hits.assign(hit_type=hit_type)
# Group by inning and hit type
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')
# Convert hit type to a categorical column
hits['hit_type'] = pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])
# Sort values
hits = hits.sort_values(['inning', 'hit_type'])
# Reshape the hits DataFrame for plotting
hits = hits.pivot(index='inning', columns='hit_type', values='count')
# Use a stacked bar chart
hits.plot.bar(stacked=True)

plt.show()
