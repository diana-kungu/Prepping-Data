#Import Libraries
from pandas import ExcelFile, read_excel, merge, pivot_table, melt
from numpy import where, timedelta64

#READ DATA
with ExcelFile(r'.\2021\Week - 47\Inputs\top_female_poker_players_and_events.xlsx') as xl :
    df = read_excel(xl, sheet_name = 'top_100', usecols=[0,1,2,3,5,7,8] )
    events = read_excel(xl, sheet_name = 'top_100_poker_events' )

# PROCESS DATA
#Add the player names to their poker events
df = merge(events, df, how='left', on='player_id')
#Create a column to count when the player finished 1st in an event
df['Won flag'] = where(df['player_place']== '1st', 1,0)
#Replace any nulls in prize_usd with zero
df['prize_usd'].fillna(0, inplace=True)
#Find the dates of the players first and last events
df['First Event'] = df.groupby(['name'])['event_date'].transform(min)
df['Last Event'] = df.groupby(['name'])['event_date'].transform(max)
# calculate the length of poker career in years (with decimals)
df['length of career'] = df['Last Event'] - df['First Event']
df['length of career']  =df['length of career'] /timedelta64(1, 'Y')

''' Create an aggregated view to find the following player stats:
Number of events they've taken part in
Total prize money
Their biggest win
The percentage of events they've won
The distinct count of the country played in
Their length of career'''

df = df.groupby(['name']).agg(Country_Played_In = ('event_country', 'nunique'),
                            Total_Prize_Money = ('prize_usd', 'sum'),
                            Biggest_win = ('prize_usd', 'max'),
                            Length_of_Career = ('length of career', 'mean'),
                            Number_of_Events =('event_date', 'count'),
                            Percent_of_Events_won=('Won flag', lambda x: x.eq(1).mean()*100)).reset_index()
col = ['Country_Played_In', 'Total_Prize_Money', 'Biggest_win','Number_of_Events']
df[col] = df[col].astype('Int32') 

# Reshape summary metrices (raw values)
df_melted = melt(df, id_vars='name', var_name='Metric', value_name='raw_value')
# rank summary stats from 1-100, with 100 representing the highest value
df[df.columns[1:]] = df[df.columns[1:]].rank()
df_ranks = melt(df, id_vars='name', var_name='Metric', value_name='scaled_value')
#Join Ranks and summary dataframes
summary = merge(df_melted, df_ranks, how='inner')


#OUTPUT
summary.to_csv(r'.\2021\Week - 47\Output\Week-47-Output.csv', index=False)
print('end')


