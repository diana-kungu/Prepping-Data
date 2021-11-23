
#Imports
from pandas import read_csv, pivot_table, DataFrame
from numpy import where


#READ DATA
df = read_csv(r'.\2021\Week - 32\PD_wk32_input.csv',
         parse_dates = ['Date','Date of Flight'], dayfirst=True)

#Form Flight name
df['Flight'] = df.Departure +' to ' +df.Destination
df.drop(['Departure', 'Destination'], axis=1, inplace=True)

#Workout how many days between the sale and the flight departing
df['Time diff'] = df['Date of Flight'] - df['Date']
df['Time diff'] = df['Time diff'].astype('str').str.strip('days').astype('int')

#Classify daily sales of a flight as: Less than 7 days before departure
#7 or more days before departure
df['Less than 7?'] = where(df['Time diff'] < 7, 1, 0)

# Reshape dataframe and aggregate Ticket Sales
df = df.pivot_table(index= ['Flight', 'Class'], columns='Less than 7?', 
values='Ticket Sales', aggfunc=['sum', 'mean'])
df = DataFrame(df.to_records())

cols_names = ['Flight', 'Class', 'Sales 7 days of more until the flight',
                'Sales less than 7 days until the flight',
                'Avg. daily sales 7 days of more until the flight', 
                'Avg. daily sales less than 7 days until the flight']
df.columns = cols_names
# Format Avg values to zero decimals places
df.iloc[:,-2:] =df.iloc[:,-2:].applymap(lambda x: int(round(x, 0)))
df

#Output
df.to_csv(r'.\2021\Week - 32\week32_output.csv', index=False)
print('End')


