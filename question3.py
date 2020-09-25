#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Rosicky Li
"""Create an aggregate dataset `agg_specialization_status.csv` containing number of unique players and percentage of them grouped by date range and specialization. Dataset columns:

- `date_range`
- `specialization` (First letter uppercase and the rest lowercase)
- `number_of_unique_players`
- `percent` (Percentage of `number_of_unique_players` in `date_range`)
Requirements:
- Dataset should contain players who **log in** between **2019-12-25 00:00:00 and 2020-02-24 23:59:59** and has ever equipped any specialization.
- There should be 2 possible values in `date_range` column: `before_CNY_2020` and `after_CNY_2020`.
  - `before_CNY_2020` includes players who **log in** between **2019-12-25 00:00:00 and 2020-01-24 23:59:59**
  - `after_CNY_2020` includes players who **log in** between **2020-01-25 00:00:00 and 2020-02-24 23:59:59**
- After a player equips a specialization, it remains as the player's specialization status until the player equips another one.
- If there are several rows for a player on a given `date_range`, the dataset should include the latest one only."""
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.DataFrame(pd.read_csv('C:/Users/admin/Desktop/specializationequip.csv'))
df['specialization_name'] = df['specialization_name'].str.capitalize()
df["date_time"] = pd.to_datetime(df['date_time']).apply(lambda x: x.replace(tzinfo=None))
low = datetime(2019, 12, 25, 0)
high = datetime(2020, 2, 25, 0)
mid = datetime(2020, 1, 25, 0)
df = df[(df['date_time'] >= low) & (df['date_time'] < high)]
df['date_range'] = np.select([(np.logical_and(df['date_time'] < mid,df['date_time'] >= low)),(df['date_time'] >= mid)],['before_CNY_2020','after_CNY_2020'])
df = df.groupby(['player_id','date_range']).apply(lambda t: t[t.date_time==t.date_time.max()])
df.reset_index(drop=True, inplace=True)
df = df.groupby(['date_range','specialization_name']).agg({'player_id': pd.Series.nunique})
df['percent'] = df.groupby('date_range')['player_id'].transform('sum')
df['percent'] = df['player_id']/df['percent']
df.rename(columns={'player_id':'number_of_unique_players'}, inplace = True)
df.to_csv('C:/Users/admin/Desktop/agg_specialization_status.csv')