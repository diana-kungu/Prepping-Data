# IMPORTS
from pandas import  read_csv, concat
#from os import getcwd, chdir
from numpy import average

#chdir(r"c:\Users\DIANA\Desktop\Prepping_data")

# READ DATA
df= read_csv(r'.\Data\week26.csv', parse_dates= ["Date"], dayfirst= True)


# PROCESS DATA
#Set index 
df.set_index('Date', inplace= True)

#Sort Index
df.sort_index(inplace= True)

# 7-Day moving Average: 3 days before and 3 days after a date as well as the day itself 
# - For each Destination
df_7d = df.groupby('Destination')\
          .rolling(window = 7, min_periods=1,  center = True)\
          .agg(['sum','mean'])\
          .rename(columns={'sum': 'Rolling Week Total', 'mean': 'Rolling Week Avg'})\
          .reset_index()
df_7d.columns = [''.join(column).replace('Revenue', "") for column in df_7d.columns.to_flat_index()]

#Groupby Date and sum Revenue for all destinations
df_all =  df.groupby('Date')['Revenue'].sum()\
                .rolling(window = 7, min_periods=1,  center = True).agg(['sum','count'])\
                        .rename(columns={'sum': 'Rolling Week Total', 'count': 'Count'}).reset_index()

#Flatten and rename columns
df_all.columns = [''.join(column).replace('Revenue', "") for column in df_all.columns.to_flat_index()]

#Compute Rolling Week Average: Rolling Week Total/ No. of days in the window * Number of unique Destinations
df_all['Rolling Week Avg']  = df_all['Rolling Week Total']  /(df_all['Count']* df.Destination.nunique())  

# Add Destination Column
df_all['Destination'] = 'All'
df_all.drop('Count', axis = 1, inplace= True)

#Merge All destinations dataframe with Daily/Destination dataframe
df = concat([df_all,df_7d])

# OUTPUT
# Reeorder columns in final dataframe
output_cols = [3, 0, 2, 1]
df = df[[df.columns[i] for i in output_cols]]

# Save Output
df.to_csv(r'./Output/week_26_output.csv', index= False)


