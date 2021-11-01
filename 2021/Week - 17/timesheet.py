#Imports
from pandas import read_excel, Series, pivot_table, crosstab
from os import chdir

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#Read Data
df = read_excel(r'.\Data\timesheet.xlsx')

#Process Data
#Drop total rows 
total = df[df['Project'].str.contains('Overall Total')].index
df.drop(total, axis=0, inplace= True)
#Pivot Dates cols
idx_cols = ['Name, Age, Area of Work', 'Project']
df_melted = df.melt(id_vars= idx_cols, var_name= 'Date', value_name= 'Hours')
#Split the expand first column
df_melted[['Name', 'Age :Area of Work']] = df_melted['Name, Age, Area of Work'].str.split(',', expand= True)
df_melted[['Age', 'Area of Work']] = df_melted['Age :Area of Work'].str.split(':', expand= True)
df_melted.drop(['Name, Age, Area of Work', 'Age :Area of Work'], axis=1, inplace= True)
#Remove annual leave rows
leave_idx = df_melted[df_melted['Hours'] == 'Annual Leave'].index
df_melted.drop(leave_idx, axis=0, inplace= True)
#Change data type and fill Nans 
df_melted['Hours'] = df_melted['Hours'].astype(float)
df_melted.fillna(0,inplace= True)
#Total up the number of hours spent on each area of work for each date by each employee.
agg = df_melted.groupby(['Name', 'Date', 'Project']).aggregate\
                        (Hours = ('Hours', sum)).reset_index()
summary= agg.groupby(['Name']).agg(\
                            Days_Worked=('Date', Series.nunique),
                            Total_Hours=('Hours', sum)).reset_index()  
 
summary['Avg Number of hours Worked per day'] = summary['Total_Hours']/summary['Days_Worked']

#Exclude Chats activities/aggregate no. of hours
chats_excld =df_melted.drop(df_melted[df_melted['Area of Work'].str.contains('Chats')].index, axis= 0)
chats_excld = chats_excld.groupby(['Name', 'Area of Work'])['Hours'].sum().reset_index()
chats_excld['Total'] =(chats_excld['Hours'] /chats_excld.groupby(['Name'])['Hours'].transform('sum'))\
                        .map('{:.0%}'.format)
clients = chats_excld[chats_excld['Area of Work'] == ' Client']
clients.drop('Hours', axis=1, inplace= True)

#Merge
df_clients = clients.merge(summary.iloc[:, [0, -1]], how='left', on='Name')

#Output
df_clients.to_csv(r'.\Output\timesheet.csv', index = False)
