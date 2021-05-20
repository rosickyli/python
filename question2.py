"""
Create an aggregate dataset `agg_skill_combo.csv` containing the number of unique players grouped by skill combinations. Dataset columns:

- `skill_combo`
- `number_of_unique_players`
- `date_time_min` (format: 'yyyy-mm-dd hh:mm:ss')
- `date_time_max` (format: 'yyyy-mm-dd hh:mm:ss')

Requirements:

- Skill combinations are expected to be **skill a + skill b**, for example **drone + hive**.
- For players who only equip one skill then skill combo is **skill a**, for example **drone**.
- It doesn’t matter if players equip the skill on left or right slot, we consider it is the same skill combination regardless of the slot. Which means **drone + hive** equals **hive + drone** and only one version of the combination should appear in the dataset.
- Players who do not equip any skill are not included in the dataset.
- `date_time_min` and `date_time_max` correspond to the date range of the aggregated dataset, hence should have a constant value for each row of the dataset.
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(pd.read_csv('C:/Users/admin/Desktop/playerstatus.csv'))
df["date_time"] = pd.to_datetime(df['date_time']).apply(lambda x: x.replace(tzinfo=None).strftime('%Y-%m-%d  %H:%M:%S'))
df = df.fillna('0')
df.loc[df['skill_left'] <= df['skill_right'], 'skill_left'] = df['skill_right']
df.loc[df['skill_left'] <= df['skill_right'], 'skill_right'] = df['skill_left']
df['skill'] = df['skill_left']+'+'+df['skill_right']
df['skill'] = df['skill'].replace('[^a-z]',' ',regex=True).str.rstrip().replace("\\s+",'+',regex=True)
df['date_max'] = df['date_time']
df = df.groupby(['skill']).agg({'date_time':'min','date_max':'max','player_id': pd.Series.nunique})
df.rename(columns={'date_time':'date_min','player_id':'number_of_unique_players'}, inplace = True)
df.to_csv('C:/Users/admin/Desktop/agg_skill_combo.csv')
