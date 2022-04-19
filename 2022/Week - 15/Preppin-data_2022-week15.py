
#Load libraries
from pandas import read_csv, merge, date_range, pivot_table
from datetime import timedelta, datetime
from numpy import timedelta64 as td, where


#Read Data
df = merge(read_csv(r'.\2022\Week - 15\Input\Rental Contracts.xlsx - Sheet1.csv', 
                    parse_dates=['Contract Start', 'Contract End'], dayfirst= True),
           read_csv(r'.\2022\Week - 15\Input\Office Space Prices.xlsx - Sheet1.csv')
           )

# PROCESS
#Parse the first and the last month of each contract in months
df['Contract End Month'] = df['Contract End'].apply(lambda x: 
                        (x.replace(day=1) -timedelta(days=1)).replace(day=1))
df['Contract Start Month'] = df['Contract Start'].apply(lambda x: 
                        x.replace(day=1))

#Calculate the length of each contract and Months until  expiry in months
df['Contract Length'] = ((df['Contract End'] - df['Contract Start'])
                         /td(1, 'M')).round().astype('int')
df['Months Until Expiry'] = ((df['Contract End'] - datetime(2022,4,13))
                         /td(1, 'M')).round().astype('int')
#Create a row for each month that a rental contract will be live
df['Month Divider'] = [date_range(s, e, freq='MS') for s, e in
              zip(df['Contract Start Month'],df['Contract End Month'])]
df = df.explode('Month Divider')
#Calculate the cumulative monthly cost of each office space contract
df['Cumulative Monthly'] = df.groupby('Company')['Rent per Month'].cumsum()

# Current date Flag: Dates less than current date
df['Current?'] = where(df['Month Divider'] <= datetime.now(), 'EoY and Current', 'Not')

#Create a table that details total rent paid for completed years
# across all contracts and year to date figures for the current 
# year, which would update as time goes on
EoY_df = (pivot_table(df.assign(Year=df['Month Divider'].dt.year), index='Year',
            columns='Current?', values='Rent per Month', aggfunc='sum')
            .reset_index()
            .rename_axis(None, axis='columns')
            .drop('Not', axis=1)
)

#OUTPUT
df.to_csv(r'.\2022\Week - 15\Output\rental_contracts.csv', index= False)
EoY_df.to_csv(r'.\2022\Week - 15\Output\Yearly_cumulative.csv', index= False)
print('End')


