# Import
from pandas import read_csv,  melt


#READ Data
df_trans = read_csv(r'.\Input Data\PD 2021 WK 1 to 4 ideas - Preferences of Travel.csv')

# Process data
#Melt 
df_trans = df_trans.melt('Student ID', var_name='Weekday', value_name='Method of Travel')

#cleans modes of transport spelling
modes = {'Bicycle': ['Bicycle', 'Bycycle'],
         'Car': ['Car', 'Carr'],
         'Scooter': ['Scooter','Scootr', 'Scoter'],
         'Walk': ['Walk', 'WAlk', 'Wallk', 'Walkk', 'Waalk'],
         'Helicopter': ['Helicopeter', 'Helicopter'],
         "Dad's Shoulders": "Dad's Shoulders",
         "Mum's Shoulders": "Mum's Shoulders", 'Aeroplane': 'Aeroplane', 
         'Skipped': 'Skipped', 'Jumped': 'Jumped', 'Hopped':'Hopped', 'Van': 'Van'}

df_trans['Method of Travel']=  [i for x in df_trans['Method of Travel'] for i,j in modes.items() if x in j ]

# Map modes of transport as either sustainable or not
sustainable = {'Sustainable': [
    'Bicycle', 'Walk', 'Scooter', 'Dad\'s Shoulders', 'Mum\'s Shoulders', 'Skipped', 'Hopped', 'Jumped'],
 'Non-Sustainable': ['Car', 'Van', 'Aeroplane', 'Helicopter']}
df_trans['Sustainable?']=  [i for x in df_trans['Method of Travel'] for i,j in sustainable.items() if x in j ]

#Groupby and aggregate
df_trans['Trips per day'] = df_trans.groupby('Weekday')['Student ID'].transform('count')
df_trans = df_trans.groupby(['Sustainable?', 'Method of Travel', 'Weekday', 'Trips per day']).agg(
    trips = ('Student ID', 'count')).reset_index()
df_trans['% of Trips per day'] = round(df_trans['trips'] /df_trans['Trips per day'],2)


#Output
df_trans.to_csv(r'.\Week - 4\Output\week4-output.csv') 


