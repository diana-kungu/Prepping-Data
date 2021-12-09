
#Imports
from pandas import read_csv, DateOffset, date_range


#Read Data
df = read_csv(r'.\2021\Week - 37\Input\phone_contracts.csv', parse_dates=['Start Date'])

#Process Date
#Create Date range : start-end of contract
df['End Date'] =[date_range(x, periods = n, freq=DateOffset(months =1 )) for x,n in 
                 zip(df['Start Date'], df['Contract Length (months)'])]

df = df.explode('End Date').drop(columns=['Start Date', 'Contract Length (months)'])\
                           .rename(columns={'End Date': 'Payment Date'})\
                           .reset_index()\
                           .drop(columns=['index'])

# Cumulative cost
df['Cumulative Monthly Cost'] = df.groupby(['Name'], as_index = False)['Monthly Cost'].cumsum()

# Output
df.to_csv(r'.\2021\Week - 37\Output\Week-37-output.csv', index=False)
print('End')

