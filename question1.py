#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Rosicky Li
"""Create an aggregate dataset `agg_skill_date.csv` containing daily number of unique players grouped by skill. Dataset columns:
- `date` (format: yyyy-mm-dd)
- `skill`
- `number_of_unique_players`
Requirements:
- It does not matter if the player equips a skill on left or right slot, we consider it is the same skill regardless of the slot.
- Players who do not equip any skill are not included in the dataset.
- If there are several rows for a player on a given day, keep the latest row only."""
import pandas as pd
import numpy as np

df = pd.DataFrame(pd.read_csv('C:/Users/admin/Desktop/playerstatus.csv'))
df['date'] = pd.to_datetime(df['date_time']).dt.normalize().map(lambda x:x.strftime('%Y-%m-%d'))
df = df.groupby(['player_id','date']).apply(lambda t: t[t.date_time==t.date_time.max()])
df.set_index(['player_id','date'],inplace=True)
df = pd.DataFrame(pd.concat([df.skill_left, df.skill_right]), columns=['skill']).reset_index()
df = df[df['skill'].notnull()]
df.reset_index(drop=True, inplace=True)
df = df.groupby(['date','skill']).agg({'player_id': pd.Series.nunique})
df.rename(columns={'player_id':'number_of_unique_players'}, inplace = True)
df.to_csv('C:/Users/admin/Desktop/agg_skill_date.csv')