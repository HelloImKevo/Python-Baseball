#!/usr/bin/env python3

import os
import glob

import pandas as pd

# Returns a tuple.
# Example: '/Users/john/GitProjects/Python-Baseball/stats', 'data.py'
path, file_name = os.path.split(os.path.abspath(__file__))
game_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'games', '*.EVE'))
game_files.sort()

game_frames = []
# Append game frames
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names=['type', 'multi2', 'multi3', 'multi4', 'multi5', 'multi6', 'event'])
    game_frames.append(game_frame)

# Concatenate DataFrames
games = pd.concat(game_frames)

# Clean values
games.loc[games['multi5'] == '??', ['multi5']] = ''

# Extract identifiers
identifiers = games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
# Forward fill identifiers
identifiers = identifiers.fillna(method='ffill')
identifiers.columns = ['game_id', 'year']

# Concatenate identifier columns
games = pd.concat([games, identifiers], sort=False, axis=1)
# Fill NaN (Not a Number) values
games = games.fillna(' ')
games.loc[:, 'type'] = pd.Categorical(games.loc[:, 'type'])

# Print DataFrame
print(games.head())
