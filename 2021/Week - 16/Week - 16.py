#IMPORTS
from pandas import read_excel, DataFrame
from numpy import where


#Read Data
league = read_excel(r'.\Data\PL Fixtures.xlsx', parse_dates=['Date'])

#PROCESS DATA

#Drop NAs
league = league.dropna(how = 'any').reset_index(drop = True)

#Split Results column
league[['Home Team Goals', 'Away Team Goals']] = league['Result'].str.split('-', expand= True).astype(int)

#Create new field Feature and Outcome
league['Fixture'] = league['Home Team'] +' - '+ league['Away Team']
league.drop(['Location', 'Result', 'Round Number', 'Date'], axis=1, inplace= True)
league['Outcome'] = where(league['Home Team Goals'] > league['Away Team Goals'], 'Home',\
                    where(league['Home Team Goals'] < league['Away Team Goals'], 'Away',\
                        'Draw'))

#Melt DataFrame
value_vars = ['Home Team', 'Away Team']
df = league.melt(id_vars=[c for c in league.columns if c not in value_vars], value_name= 'Team')    

df['Total Goals Scored'] = where(df['variable']== 'Home Team', df['Home Team Goals'],
                            df['Away Team Goals'])
df['Goals Conceded'] = where(df['variable']== 'Home Team', df['Away Team Goals'],df['Home Team Goals'])
df['Total Games Played'] = 1

big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Man Utd', 'Man City', 'Spur']

df['Points']= where(df['Total Goals Scored'] > df['Goals Conceded'], 3,\
                where(df['Total Goals Scored'] < df['Goals Conceded'], 0, 1))
df['Goal Difference'] = df['Total Goals Scored'] - df['Goals Conceded']


#League without the big six
cols = ['Goal Difference', 'Points', 'Total Games Played']
teams_1 = df.groupby('Team')[cols].sum().reset_index().sort_values(by= 'Points', ascending= False)
df_a =[~df['Fixture'].str.contains(i) for i in big_6]
df_2 = df[all(df_a, axis= 0)]

teams_2 = df_2.groupby('Team')[cols].sum().\
                    reset_index().sort_values(by= 'Points', ascending= False)

#Ranking
rank_cols = ['Points', 'Goal Difference']
teams_1['Position'] = teams_1[rank_cols].apply(tuple, axis= 1)\
                        .rank(method='min', ascending= False).astype('int')
teams_2['Position'] = teams_2[rank_cols].apply(tuple, axis= 1)\
                        .rank(method='min', ascending= False).astype('int')

#Merge
teams_2 = teams_2.merge(teams_1[['Team', 'Position']], how='left', on= 'Team', suffixes=('', '_v2'))
teams_2['Position Change'] = teams_2['Position_v2'] - teams_2['Position']
teams_2.drop('Position_v2', axis= 1, inplace= True)

#Output
teams_1.to_csv(r'.\Output\pl.csv', index = False)
teams_2.to_csv(r'.\Output\esl.csv', index = False)

