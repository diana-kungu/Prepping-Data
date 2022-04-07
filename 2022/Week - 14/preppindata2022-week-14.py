# Week 14

#Import libraries
from pandas import read_csv
from numpy import where


# Load data and keep relevant fields
df = (read_csv(r'.\2022\Week - 14\Input\Richard Osmans House of Games - Episode Guide - Players.csv').
    drop(["*Scoring Rate = % of Total Daily Points Scored Across Week",
         'Avg', 'Rate*', 'M.1', 'T.2', 'W.1', 'T.3', '1st', '2nd', '3rd',
         '4th', 'Ser..1', 'Wk..1', '4-Player Total', 'Seat'], axis=1).
    dropna(how='all', axis=1)
)

#  Rename certain fields to remove duplication
df.rename(columns = {'Ser.': 'Series', 'Wk.': 'Week', 'T': 'Tu', 'T.1': 'Th',
    'Total': 'Score', 'Week': 'Points', 'Week.1': 'Original Rank', 'F.1': 'Fri Rank'}, inplace = True)


# Filter the data to remove Series that have a null value, or are preceded by an 'N'
df = df[~((df.Series.str.contains('^N', regex= True, na=False)) |
   (df['Series'].isna()))]

# Extract int rank postion from str
df['Original Rank'] = df['Original Rank'].str[0].astype(int)

#Calculate the Points without Friday double points 
df['Points without double points Friday'] = where(df['Fri Rank'] =='1st', df['Points'] -4,
                                            where(df['Fri Rank'] =='2nd', df['Points'] -3, 
                                            where(df['Fri Rank'] =='3rd', df['Points'] -2,
                                            df['Points'] -2))
                                            )
#Calculate the Score if the score on Friday was doubled
df['Score if double score Friday'] = df['Score'] + df['F']
                                
# Rank the players based on Score, Score if double, and Points without double
df['Rank without double points Friday'] = (df.groupby(['Series', 'Week'])
                                            ['Points without double points Friday']
                                            .rank("dense", ascending=False)
                                            .astype('int')
                                            )

df['Rank based on Score'] = (df.groupby(['Series', 'Week'])
                             ['Score'].rank("dense", ascending=False).astype('int'))
df['Rank if Double Score Friday'] = (df.groupby(['Series', 'Week'])
                             ['Score if double score Friday'].rank("dense", ascending=False).astype('int'))

#Create fields to determine if there has been a change in winner for that particular Series 
# and Week for each Score, Score if double, and Points without double ranks
df['Change in winner with no double points Friday?'] = df['Original Rank'] == df['Rank without double points Friday']
df['Change in winner based on Score?'] = df['Original Rank'] == df['Rank based on Score']
df['Change in winner if Double Score Friday?'] = df['Original Rank'] == df['Rank if Double Score Friday']

# OUTPUT
cols = ['Series', 'Week', 'Player', 'Original Rank', 'Rank without double points Friday',
    'Rank based on Score', 'Change in winner based on Score?', 'Rank if Double Score Friday',
    'Change in winner if Double Score Friday?', 'Points', 'Score', 'Points without double points Friday',
    'Score if double score Friday']

df.to_csv(r'.\2022\Week - 14\Output\Richard House og Games-Output.csv', columns=cols, index =False)

print('End')
