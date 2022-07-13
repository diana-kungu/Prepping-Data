# Preppin Data week 28
#Load libraries
from pandas import read_csv, merge, DataFrame, date_range

#Read Data
df = read_csv(r".\2022\Week - 28\Input\Preppin' Summer 2022 - PD 2022 Wk 27 Input(1).csv",
              parse_dates=['Sale Date'], dayfirst= True)

#Create a new row for each day in the sale date range
days = DataFrame(date_range(start= df['Sale Date'].min(), end= df['Sale Date'].max()), 
          columns= ['Sale Date'] )
df = df.merge(days, how= 'outer')

#Create a column for Day of the Week
df['Day of the week'] = df['Sale Date'].dt.day_name()

#Remove any date record where a sale occurred
df = df[df['Sale Value'].isna()]
#For each day of the week, count the numbers of dates where there were no sales
df = df.groupby('Day of the week')['Sale Date'].nunique().reset_index().rename(columns={
    'Sale Date': 'Number of Days'})

#OUTPUT
df.to_csv(r'.\2022\Week - 28\Output\Week28_output.csv', index = False)
print('prepped!')


