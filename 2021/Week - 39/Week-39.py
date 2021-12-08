#Imports
from pandas import read_csv, pivot_table, Series, merge
from datetime import datetime as dt
from numpy import where, nan


#Read Data
df = read_csv(r'.\2021\Week - 39\Input\Bike Painting Process - Painting Process.csv')


#Process Data
df['Datetime'] = df['Date'] +', '+ df['Time']
df['Datetime'] = df['Datetime'].apply(lambda x: dt.strptime(x, '%d/%m/%Y, %H:%M:%S')) 
df.drop(['Date', 'Time'], axis=1, inplace= True)


#Extract bike-status information
df_bike = df.iloc[where (df['Data Type'] == 'Result Data')]
bike_status = pivot_table(df_bike, index=['Batch No.'], columns='Data Parameter',
                          values='Data Value', aggfunc='first').reset_index()
# Name of process field and forward fill
df['Name of Process Step'] = Series(where(df['Data Parameter']=='Name of Process Stage', 
                                          df['Data Value'], nan)).fillna(method='ffill')
# Create Actual vs Target fields
actual_target = ['Name of Process Stage', 'Batch Status', 'Bike Type']
df_actl_trgt = df.iloc[where(~df['Data Parameter'].isin(actual_target))].copy()
df_actl_trgt['Actual_Target'] = where(df_actl_trgt['Data Parameter'].str.contains('Target'), 
                     'Target', 'Actual')
df_actl_trgt['Data Parameter'] = df_actl_trgt['Data Parameter'].apply(lambda x:
                                        x.split()[1])
df_actl_trgt = pivot_table(df_actl_trgt, 'Data Value', index=['Batch No.', 'Datetime',
                                                              'Data Parameter', 'Name of Process Step'],
                           columns= 'Actual_Target', aggfunc='first').reset_index()

# Combine
df_combined = merge(df_actl_trgt, bike_status, how='left') 

#OUTPUT
df_combined.to_csv(r'.\2021\Week - 39\Output\week-39-output.csv', index= False)
print('End')