
#Imports
from pandas import ExcelFile, read_excel, concat, to_datetime
from datetime import datetime, timedelta
from numpy import where


#READ DATA
with ExcelFile(r'.\2021\Week - 33\Allchains Weekly Orders.xlsx') as xl :
    df = concat([read_excel(xl, sheet_name = s ).assign(
                Report_Date = s) for s in xl.sheet_names], ignore_index=True)


#Create date from Report_Date
df['Report_Date'] =to_datetime(df['Report_Date'])


#Find the Minimum and Maximum date where an order appeared in the reports
grouper = df.groupby(['Orders'])
df = df.assign(min=grouper['Report_Date'].transform('min'),
                        max=grouper['Report_Date'].transform('max'))
df['Fullfilled by'] = df['max'] + timedelta(days=7)

# Create Order Status by the following logic:
# The first time an order appears it should be classified as a 'New Order'
#The week after the last time an order appears in a report (the maximum date) 
# is when the order is classed as 'Fulfilled' 
# Any week between 'New Order' and 'Fulfilled' status is classed as an 'Unfulfilled Order' 
df['Order Status'] = where(df['Report_Date'] == df['min'], 'New Order',
                    where(df['Report_Date'] > df['max'], 
                    'Fulfilled', 'Unfulfilled'))
df.sort_values(by= 'Orders', inplace=True)

# Find all fulfilled orders
fulfilled = df.loc[(df['Report_Date']==df['max']) 
                   & (df['Report_Date'] != df['Report_Date'].max())].copy()

fulfilled['Order Status'] = 'Fulfilled'
fulfilled.drop(['min', 'max', 'Report_Date'], axis=1, inplace = True)
fulfilled.rename(columns={'Fullfilled by': 'Report_Date'}, inplace = True)

# Join fulfilled orders to other dataframe
df.drop(['min', 'max', 'Fullfilled by'], axis=1, inplace = True)
df = concat([df, fulfilled], ignore_index=True)


#OUTPUT
df.to_csv(r'.\2021\Week - 33\week33_output.csv', index=False)
print('End')

