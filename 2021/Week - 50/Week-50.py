# Import Libraries
from pandas import melt, ExcelFile, read_excel, concat
from numpy import where

# Read Data
with ExcelFile(r'.\2021\Week - 50\Input\Sales Department Input.xlsx') as xl :
    df2 = concat([read_excel(xl, sheet_name = s , parse_dates=['Date'], index_col='RowID' )
                  for s in xl.sheet_names], ignore_index= True)
    
#Process 
#Fill in the Salesperson names for each row    
df2['Salesperson'] = df2['Salesperson'].fillna(method='bfill')
df2.rename(columns={'Unnamed: 7': 'YTD'}, inplace=True)
df2['YTD'] = df2['YTD'].fillna(method='bfill')
df2.dropna(how='any', subset=['Date'], inplace=True)

df2['Month'] = df2.Date.dt.month
df2['Monthly Total'] = df2.groupby(['Salesperson', 'Month'] ).Total.transform('sum')
df2['YTD'] = where(df2['YTD'].isna(), df2['Monthly Total'], df2['YTD'])

# from the October YTD, create YTD totals for November| other months
ytd = df2.groupby(['Salesperson', 'Month'])['YTD'].max().groupby(level=0).cumsum().reset_index()
df2 = df2.merge(ytd, how='left', left_on=['Salesperson', 'Month'], right_on=['Salesperson', 'Month'],
                suffixes = ('_x', ''))
df2.drop(['Total', 'YTD_x', 'Month', 'Monthly Total'], axis=1, inplace= True)

# Reshape the data so all the bike types are in a single column
df2 = df2.melt(id_vars = ['Date', 'Salesperson', 'YTD'], value_vars=['Road', 'Gravel', 'Mountain'], value_name = 'Sales', 
               var_name= 'Bike Type')

#Output
df2.to_csv(r'.\2021\Week - 50\Output\week-50-output.csv', index = False)
print('End')

