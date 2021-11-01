from pandas import read_excel, DataFrame
from os import chdir
from datetime import timedelta, date

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

df= read_excel(r'.\Data\Wk18.xlsx', parse_dates=['Scheduled Date'])


#Completed Date
df['Completed Date'] = df.apply(lambda row: row['Scheduled Date'] + timedelta(\
                                days= row['Completed In Days from Scheduled Date']), axis= 1)

df.rename(columns={'Completed In Days from Scheduled Date':'Days Difference to Schedule'}, inplace= True)
df_complete = df.pivot(index= ['Project', 'Sub-project', 'Owner'], columns='Task', values='Completed Date').reset_index()
df_complete['Scope to Build Time'] =  df_complete['Build'] - df_complete['Scope']
df_complete['Build to Delivery Time'] =  df_complete['Deliver'] -  df_complete['Build']


df = df.merge(df_complete[['Project', 'Sub-project',	'Owner', 'Scope to Build Time', 'Build to Delivery Time' ]],\
                    on= ['Project', 'Sub-project',	'Owner'], how= 'inner')

df['Completed Weekday'] = df['Completed Date'].dt.day_name()
out_cols = [9, 2, 7, 8, 5, 0, 1, 3, 4, 6]
df = df[[df.columns[i] for i in out_cols]]

#OUTPUT
df.to_csv(r'.\Output\wk18output.csv', index = False)