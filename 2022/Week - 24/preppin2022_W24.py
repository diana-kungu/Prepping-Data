
#Load libraries
from pandas import ExcelFile, read_excel, to_datetime, merge

#Load Data
with ExcelFile(r'.\2022\Week - 24\Input\2022W24 Inputs.xlsx') as xl :
    df_flights = read_excel(xl, sheet_name = 'Non-stop flights' )
    cities = read_excel(xl, sheet_name = 'World Cities' )


#------------------------------------------------------------------------
#PROCESSING
#Remove the airport names from the From and To fields
df_flights['To'] = [val[0] for val in df_flights['To'].str.split('–|-|/')]
df_flights['From'] = [val[0] for val in df_flights['From'].str.split('–|-|/')]

#Create a Route field which concatenates the From and To fields with a hyphen
df_flights['Route'] = df_flights['From'] + ' - ' + df_flights['To']

#Split out the Distance field to Distance in km and Distance in miles
df_flights['Distance - km'] = df_flights['Distance'].str.extract(r'(.*)(?=\skm)')
df_flights['Distance - mi'] = df_flights['Distance'].str.extract(r'(?<= km \()(.*)(?= mi)')

df_flights[['Distance - km', 'Distance - mi']] = df_flights[['Distance - km', 'Distance - mi']].apply(
    lambda x: x.str.replace(',', '').astype(int), axis=1 # convert to integer
)

#Rank the flights based on Distance
df_flights['Rank'] = df_flights['Distance - km'].rank(method='dense', ascending= False).astype(int)

#Update the First flight field to be a date
df_flights['First flight'] = to_datetime(df_flights['First flight'] )

#Merge with world cities dataframe
df_flights = (df_flights.merge(cities, left_on= 'From', right_on= 'City', how ='left').rename(columns=
                                                                   {'Lat': 'From Lat',
                                                                    'Lng': 'From Lng'})
              .merge(cities, left_on= 'To', right_on= 'City', how ='left').rename(columns=
                                                                   {'Lat': 'To Lat',
                                                                    'Lng': 'To Lng'})
              
)
# remove unwanted columns
df_flights.drop(['Distance', 'City_x', 'City_y'], axis=1, inplace= True)

df_flights.sort_values(by='Rank', inplace= True)
#------------------------------------------------------------------------------------------------------

#OUTPUT
df_flights.to_csv(r'.\2022\Week - 24\Output\week_24.csv', index= False)

