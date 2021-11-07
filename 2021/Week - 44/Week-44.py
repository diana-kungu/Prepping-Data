#Imports
from pandas import read_excel, pivot_table, date_range, to_datetime
from os import getcwd, chdir
from numpy import where

chdir(r'c:\Users\DIANA\Desktop\Prepping_data')

#READ DATA
df =read_excel(r".\Data\Carl's 2021 cycling.xlsx")

#PROCESS DATA

#Format Date
df['Date'] = to_datetime(df['Date'], dayfirst= True)

#Create a field to convert Measure field to: Turbo Trainer(Min) and Outdoor (KM)
df['Type'] = ['Outdoor' if df['Measure'][i] == 'km'
                        else 'Turbo Trainer' for i in range(df.shape[0])]
#Convert Mins to Km: 30KM/Hour
df['Value'] = where(df['Measure'] == 'min', (df['Value']/60)*30, df['Value'])

#Count number of activities per day
df['Activities per day'] = df.groupby(['Date', 'Type'])['Measure'].transform('count')

#Reshape dataframe by Activity Type
df = pivot_table(df, index= ['Date', 'Activities per day'], columns= 'Type', values= ['Value'],
                    aggfunc= {'Value': 'sum'}, fill_value= 0).reset_index()
df.columns = [''.join(col).strip() for col in df.columns.values]

#Create Date Range 01/01/2021 - 01/11/2021 to get all days without workout
idx = date_range(df.Date.min(), df.Date.max())
df.set_index('Date', inplace=True)
df = df.reindex(idx, fill_value=0).reset_index().rename(columns={'index': 'Date'})

df.columns = [c.replace('Value', '') for c in df.columns]



#OUTPUT
df.to_csv(r'.\Output\week44.csv')