#IMPORTS
from pandas import read_csv
from numpy import std, where


#READ DATA
df =read_csv(r'.\Data\prep-air-complaints.csv', parse_dates=['Date'])

#PROCESS DATA

#Calculate Mean and Std
df['Mean'] = df.groupby(['Week'])['Complaints'].transform('mean')
df['STD'] = df.groupby(['Week'])['Complaints'].transform('std')

# 1SD
df_1SD = df.copy()
df_1SD['Upper Control Limit'] = df_1SD['Mean'] + (1*df_1SD['STD'])
df_1SD['Lower Control Limit' ] = df_1SD['Mean'] - (1*df_1SD['STD'])
df_1SD['Variation (1SD)'] =df_1SD['Upper Control Limit'] - df_1SD['Lower Control Limit']
df_1SD['Outlier? (1SD)'] = where((df_1SD['Complaints'] >= df_1SD['Lower Control Limit']) & (\
            df_1SD['Complaints'] <= df_1SD['Upper Control Limit']), 'Within', 'Outside')
df_1SD = df_1SD[df_1SD['Outlier? (1SD)'] == 'Outside']

# 2SD
df_2SD = df.copy()
df_2SD['Upper Control Limit'] = df_2SD['Mean'] + (2*df_2SD['STD'])
df_2SD['Lower Control Limit' ] = df_2SD['Mean'] - (2*df_2SD['STD'])
df_2SD['Variation (2SD)'] =df_2SD['Upper Control Limit'] - df_2SD['Lower Control Limit']

df_2SD['Outlier? (2SD)'] = where((df_2SD['Complaints'] >= df_2SD['Lower Control Limit']) & (\
            df_2SD['Complaints'] <= df_2SD['Upper Control Limit']), 'Within', 'Outside')
df_2SD = df_2SD[df_2SD['Outlier? (2SD)'] == 'Outside']
df_2SD

# 3SD
df_3SD = df.copy()
df_3SD['Upper Control Limit'] = df_3SD['Mean'] + (3*df_3SD['STD'])
df_3SD['Lower Control Limit' ] = df_3SD['Mean'] - (3*df_3SD['STD'])
df_3SD['Variation (3SD)'] =df_3SD['Upper Control Limit'] - df_3SD['Lower Control Limit']

df_3SD['Outlier? (3SD)'] = where((df_3SD['Complaints'] >= df_3SD['Lower Control Limit']) & (\
            df_3SD['Complaints'] <= df_3SD['Upper Control Limit']), 'Within', 'Outside')
df_3SD = df_3SD[df_3SD['Outlier? (3SD)'] == 'Outside']
df_3SD

#OUTPUT
df_1SD.to_csv(r'.\Output\df_1SD.csv', index= False)
df_2SD.to_csv(r'.\Output\df_2SD.csv', index= False)
df_3SD.to_csv(r'.\Output\df_3SD.csv', index= False)


