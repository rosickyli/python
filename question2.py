import pandas as pd
import numpy as np

df = pd.DataFrame(pd.read_csv('C:/Users/admin/Desktop/playerstatus.csv'))
df["date_time"] = pd.to_datetime(df['date_time']).apply(lambda x: x.replace(tzinfo=None))
df = df.fillna('0')
df.loc[df['skill_left'] <= df['skill_right'], 'skill_left'] = df['skill_right']
df.loc[df['skill_left'] <= df['skill_right'], 'skill_right'] = df['skill_left']
df['skill'] = df['skill_left']+'+'+df['skill_right']
df['skill'] = df['skill'].replace('[^a-z]',' ',regex=True).str.rstrip().replace("\\s+",'+',regex=True)
df['date_max'] = df['date_time']
df = df.groupby(['skill']).agg({'date_time':'min','date_max':'max','player_id': pd.Series.nunique})
df.rename(columns={'date_time':'date_min','player_id':'number_of_unique_players'}, inplace = True)
df.to_csv('C:/Users/admin/Desktop/question2.csv')