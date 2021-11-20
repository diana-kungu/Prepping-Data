
from pandas import read_excel, ExcelFile, concat, to_datetime, merge, crosstab, DataFrame, to_numeric,pivot_table
from datetime import datetime, date
from numpy import where, nan, nansum
from os import chdir, getcwd
print(chdir())
chdir(r'c:\Users\DIANA\Desktop\Prepping_data')


#READ DATA
with ExcelFile(r'.\Data\InternationalPenalties.xlsx') as xl :
    wc = read_excel(xl, sheet_name = "WorldCup")
    euro = read_excel(xl, sheet_name = "Euros")
#Clean Columns names
wc.columns = [c.strip() for c in wc.columns]              
df = concat([wc, euro], ignore_index= True)


#PROCESS DATA
#.............................................................................
#Make data field
df['Event Year'] =df['Event Year'].str.strip(',').astype('int')
df['Date'] = df.apply(lambda row: row['Date'].replace(year=row['Event Year']), axis = 1)

#Group the two German countries (eg, West Germany & Germany)
df['Winner'] = ['Germany' if 'West' in x else x.strip() for x in df['Winner']]
df['Loser'] = ['Germany' if 'West' in x else x.strip() for x in df['Loser']]

#Fill Nans for penalties not taken: case when a winner is determined before 
#all kicks are taken
df[['Winning team Taker', 'Losing team Taker']] = df[
                                ['Winning team Taker', 'Losing team Taker']].fillna('Not Taken')

# Penalty Scored?
df['Winner Scored?'] = [1 if 'scored' in df['Winning team Taker'].iloc[i] 
                          else 0  for i in range(df.shape[0])]
df['Loser Scored?'] = [1 if 'scored' in df['Losing team Taker'].iloc[i]
                         else 0 if 'missed' in df['Losing team Taker'].iloc[i]
                         else nan for i in range(df.shape[0])]

df['Winner Missed?'] = [1 if 'missed' in df['Winning team Taker'].iloc[i] 
                          else 0  for i in range(df.shape[0])]
df['Loser Missed?'] = [1 if 'missed' in df['Losing team Taker'].iloc[i]
                         else 0 for i in range(df.shape[0])]

#QUUESTION ONE
#Rank the countries on the following: 
# -Shootout win % (exclude teams who have never won a shootout)

df_winners = df.copy()
df_winners = df_winners.groupby(['Winner', 'Loser', 'Date']).agg(
                                        Total_Winner_Scored=('Winner Scored?', 'sum'),
                                        Total_Loser_Scored=('Loser Scored?', 'sum'),
                                        Total_Winner_Missed=('Winner Missed?', 'sum'),
                                        Total_Loser_Missed=('Loser Missed?', 'sum')).reset_index()
wins_ = df_winners.groupby(['Winner'])['Total_Winner_Scored'].count(
                    ).to_frame().reset_index().rename(columns={'Total_Winner_Scored': 'Shootout Wins',
                                                                'Winner': 'Team'})


# 
df_melted = df_winners.melt(id_vars='Date', value_vars=['Winner', 'Loser'], var_name='Total Shootouts', value_name='Team')

df_melted = df_melted.groupby('Team')['Total Shootouts'].count().to_frame().reset_index()


# %%
(wins_)  = merge(wins_, df_melted, how='left')
wins_['Shootout Wins %'] = (wins_['Shootout Wins']*100/ wins_['Total Shootouts']).round(0).astype('int')
wins_['Win % Rank'] =  wins_['Shootout Wins %'].rank(method='dense', ascending=False).astype('int')
wins_.sort_values(by='Win % Rank', inplace=True)
wins_


#..............................................................................................
#Question Two
#.............................................................................................
#Rank the countries on the following: 
## -Penalties scored
win_cols = [c for c in df_winners.columns if 'Winner' in c]
loss_cols = [c for c in df_winners.columns if 'Loser' in c]

win = df_winners[win_cols]
loss = df_winners[loss_cols]
win.columns =['Team', 'Scored', 'Missed']
loss.columns =['Team', 'Scored', 'Missed']

penalties = concat([win,loss], axis= 0, ignore_index= True)

# 
penalties = penalties.groupby('Team', as_index=0).sum()
penalties['% Total Penalties Scored'] = ((penalties['Scored']*100)/
                                        (penalties['Scored'] + penalties['Missed'])).round(0).astype('int')
penalties['Penalties Score Rank'] = penalties['% Total Penalties Scored'].rank(method='dense', ascending= False).astype('int')
penalties.sort_values(by='Penalties Score Rank', inplace= True)

#.....................................................................................................
#QUESTION THREE
#......................................................................................................
df['Winner Scored?'] = where(df['Winning team Taker'] == 'Not Taken', nan,
                                            df['Winner Scored?'])
df['Loser Scored?'] = where(df['Losing team Taker'] == 'Not Taken', nan,
                                            df['Loser Scored?'])                                            

# 
df_pen = df.melt(id_vars='Penalty Number', value_vars=['Winner Scored?', 'Loser Scored?', 'Winner Missed?', 'Loser Missed?'])
df_pen['variable'] = df_pen['variable'].apply(lambda row: row.split()[1].strip('?'))
df_pen['value'] = to_numeric(df_pen['value'], errors = 'ignore')

# 
df_pen = df_pen.groupby(['Penalty Number', 'variable']).agg(Total = ('value', 'sum'), 
                            ).reset_index()
# 
df_pen = pivot_table(df_pen, index='Penalty Number', columns='variable').reset_index()
df_pen.columns = [' '.join(c) for c in df_pen.columns]

# %
df_pen['% Penalty Score'] = ((df_pen['Total Scored']*100)/(df_pen['Total Missed']+
                                df_pen['Total Scored'])).round(0).astype('int')
df_pen['Total Penalty Score'] = (df_pen['Total Scored'] + df_pen['Total Missed']).round(0).astype('int')
df_pen['Rank'] = df_pen['% Penalty Score'].rank(method='dense', ascending=0).astype('int')
df_pen.sort_values(by='Rank', inplace=True)


#OUTPUT
#..............................................................................................................


