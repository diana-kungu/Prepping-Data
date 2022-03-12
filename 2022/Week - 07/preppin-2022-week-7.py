# Prepping Data Week 7
#Load Libraries
from pandas import read_excel, ExcelFile, concat, merge
from datetime import datetime
from numpy import where


#READ DATA
col_names = {'Offered': 'Calls Offered', 'Not Answered': 'Calls Not Answered',
             'Answered': 'Calls Answered'}          
with ExcelFile(r'.\2022\Week - 7\Input\MetricData2021.xlsx') as xl:
    metrics = concat([read_excel(xl, s ).rename(col_names, axis=1).
                      assign(Month = s) for s in xl.sheet_names])
with ExcelFile(r'.\2022\Week - 7\Input\PeopleData.xlsx') as  pl:
    people = read_excel(pl, sheet_name = 'People' )
    leaders = read_excel(pl, sheet_name = 'Leaders' )
    locn = read_excel(pl, sheet_name = 'Location' )
    dates = read_excel(pl, sheet_name='Date Dim')
    goal = read_excel(pl, sheet_name='Goals')

# PROCESS DATA
#Join the People, Location, and Leader data sets together
df_plp = people.merge(leaders, how='left', left_on='Leader 1', right_on='id',
                      suffixes=('_agent', '_leader')).merge(locn, how='left'
                      ).drop(['id_leader', 'Location ID'], axis=1)

#Create last name, first name fields for the agent and the leader
df_plp['Agent Name'] = df_plp['first_name_agent'].str.cat(df_plp['last_name_agent'], sep=", ")
df_plp['Leader Name'] = df_plp['first_name_leader'].str.cat(df_plp['last_name_leader'], sep=", ")
df_plp.drop(['first_name_agent', 'last_name_agent', 'first_name_leader', 'last_name_leader'],
            axis= 1, inplace= True)
#Filter 2021 dates
dates = dates[dates['Month Start Date'].dt.year<2022]
#join dates dataframe to the People, Location, Leader dataframe
df_plp = df_plp.merge(dates, how = 'cross')

# create a month start date
metrics['Month'] = metrics['Month'].apply(lambda x: datetime(
                                        2021, int(datetime.strptime(x,  "%b").strftime("%m")),1))

# Join Monthly metric data to people dataframe
df = df_plp.merge(metrics, how='left', left_on=['id_agent', 'Month Start Date'],
                  right_on=['AgentID', 'Month']).drop(['AgentID', 'Month'], axis= 1)

#calculate the percent of calls offered that weren't answered
df['Not Answered Rate'] = (df['Calls Not Answered']/df['Calls Offered']).round(3)
# calculate the average duration by agent (for each agent, each month)
df['Agent Avg Duration'] = (df['Total Duration']/df['Calls Answered']).round().astype('Int64')

# Parse Goals data:-
goal['goal'] =goal['Goals'].str.extract('([A-Za-z]+\s?\w+\s?\w+)')
goal['Cut-off'] = goal['Goals'].str.extract('[A-Za-z]+\s?\w+\s?\w+\s(.+)')[0].str.split(' ')

#Add Not Answered percent and sentiment cut-off scores to the dataframe
df['Not Answered Percent'] = float(goal[goal['goal'] == 'Not Answered Percent']['Cut-off'][0][1])
df['Sentiment Score >=0'] = float(goal[goal['goal'] == 'Sentiment Score']['Cut-off'].iloc[0][1])

#  Test if the not answered percent goal goal is met
df['Met Not Answered Rate'] = where(df['Not Answered Rate'].isna(), '',
                                    df['Not Answered Rate'] < df['Not Answered Percent']/100)
#  Test if the sentiment goal goal is met
df['Met Sentiment Goal'] = where(df['Sentiment'].isna(), '',
                                 df['Sentiment'] >= df['Sentiment Score >=0'])
#Rename columns
df.rename(columns={'id_agent': 'id'}, inplace =True)
df = df.iloc[:, [0,3,1,4,5,2,8,7,12,16,14,6,9,13,15,14,15,17]]#Reorder columns

# OUTPUT
df.to_csv(r'.\2022\Week - 7\Output\week-7.csv', index = False)
print('End')


