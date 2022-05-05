
#Load libraries
from pandas import read_csv, melt, pivot_table, to_datetime


#Read data
df = read_csv(r'.\2022\Week - 18\Input\2022W18 Input.csv').melt(id_vars='Region')

#Split out the Bike Type, Date and Measure Name
df[['Bike Type', 'Date', 'Measure Name']] =df['variable'].str.split('___', expand = True)
# Format date field
df['Date'] = to_datetime('01_'+ df['Date'], format= '%d_%b_%y')

#Create a field for Sales and Profit
df = (pivot_table(df, values= 'value', index =['Region', 'Bike Type', 'Date'], 
            columns='Measure Name', aggfunc='first')
      .reset_index()
      .rename_axis(None, axis=1)
     )
# Output
df.to_csv(r'.\2022\Week - 18\Output\allchains_w18.csv', index= False)
print('End')


