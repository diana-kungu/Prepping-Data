
#Imports
from pandas import read_csv, to_datetime, DataFrame
from numpy import where

#2021\Week - 30\input-data.csv
#Read Data
df = read_csv(r'.\2021\Week - 30\input-data.csv')
df.head()

#Create a TripID field based on the time of day
# Assume all trips took place on 12th July 2021
df['Date'] = '12/07/2021'+" "+df['Hour'].astype('str')+":"+df['Minute'].astype('str')
df['Date'] = to_datetime(df['Date'])

#Set Date as index
df.set_index('Date', drop=1, inplace=True)


#Rename Ground floor and Basement to 0, -1 respectively
df['From'] = where((df['From'] == 'G'), 0,
                where(df['From'] == 'B', -1, df['From']))
df['To'] = where((df['To'] == 'B'), -1,
                where(df['To'] == 'G', 0, df['To']))                  
df[['From', 'To']] =df[['From', 'To']].astype('int')

df.drop(['Hour', 'Minute'], axis=1, inplace= True)

#Calculate how many floors the lift has to travel between trips
df['Next floor'] = df['From'].shift(-1)
df['Floor Diff']  = abs(df['Next floor']- df['To'])

#Calculate which floor the majority of trips begin at - call this the Default Position
floors = (df['From'].values).tolist()
default_pos = max([(floors.count(chr), chr) for chr in set(floors)])[1]


#How does the average floors travelled between trips compare to the average travel 
# from the default position?
avg_floors_currently = df['Floor Diff'].mean()
avg_floors_currently

# if every trip began from the same floor, how many floors would the lift need to travel to begin 
# each journey?
df['floors_diff_from_G'] = abs(df['From'].shift(-1) - default_pos)
avg_travel_from_default_Pos= df['floors_diff_from_G'].mean()

# Create output dataframe
results = DataFrame({'Default pos': default_pos,
                     "Avg travel from default Position": avg_travel_from_default_Pos,
                      'Avg travel between trips currently': avg_floors_currently}, index=[0])

# Calculate the difference
results['Difference'] = (results['Avg travel from default Position'] - 
                            results['Avg travel between trips currently'])

results
print('End')



