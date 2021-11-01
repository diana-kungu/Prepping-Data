import pandas as pd
import os

print(os.getcwd())
#os.chdir(r'..\..')
print(os.getcwd())

#READ DATA
df = pd.read_csv(r'.\Data\Tourism.csv', na_values = 'na')


#PROCESS DATA
# Transform data from wide to long format
df = df.melt(id_vars= ['id', 'Series-Measure', 'Hierarchy-Breakdown', 'Unit-Detail'], 
                        var_name= 'Month', value_name= 'Number of Tourists')

#Clean Number of Tourists and Month fields
df['Number of Tourists'] = df['Number of Tourists'].str.strip('%')
df['Number of Tourists'] = pd.to_numeric(df['Number of Tourists'], errors='coerce').astype(float)
df['Month'] = df['Month'] + '-01'
df['Month'] = pd.to_datetime(df['Month'], format= '%y-%b-%d')

#Filter out rows with Tourists information
df = df[(df['Unit-Detail'] == 'Tourists') & (df['Series-Measure']  != 'Total tourist arrivals')
                                 & (df['Number of Tourists'].notna())]
df['Series-Measure'] = df['Series-Measure'].str.replace('-', 'from')

#Create Continent/Country field
df['Continents/Country'] = df['Series-Measure'].str.extract(r'from\s(.*)')

#Separate data at Continent and Country level of detail into two dataframes
continents = ['Asia', 'Europe', 'Americas', 'Oceania', 'Africa', 'the Middle East', 'UN passport holders and others']
df_continent = df[df['Continents/Country'].isin(continents)]
df_country = df[~df['Continents/Country'].isin(continents)]

#Create Breakdown field in the country df i.e the continent of each country
df_country['Breakdown'] = df_country['Hierarchy-Breakdown'].str.extract(r'([^\s]+$)')
cols = ['Breakdown', 'Number of Tourists', 'Month', 'Continents/Country']
df_country = pd.DataFrame(df_country, columns= cols) #drop unwanted columns

#Groupby Breakdown(Continent) to obtain the total no. of tourists from each continent
Total_countries = df_country.groupby(['Breakdown', 'Month'])['Number of Tourists'].sum().reset_index()

#Merge continent df and Total_countries df and find the no. of tourists from Unknown countries in 
#each continent
df_continent = df_continent.iloc[:,[4,5,6]]
unknown_contries= df_continent.merge(Total_countries, how = 'left', left_on= ['Month', 'Continents/Country'],
                                     right_on=['Month', 'Breakdown']) #
unknown_contries.fillna(0, inplace = True)
unknown_contries['No from Unknown countries'] = unknown_contries.apply(lambda row: row['Number of Tourists_x'] 
                                                - row['Number of Tourists_y'], axis = 1)

#Rename/clean fields and merge dfs with nos. from known and unknown countries
unknown_contries['Breakdown'] = "Unknown"
unknown_contries = unknown_contries.iloc[:, [0,2,3,5]]
unknown_contries =unknown_contries.rename(columns={'No from Unknown countries': 'Number of Tourists'})
df_country = pd.concat([df_country, unknown_contries], axis = 0)


#OUTPUT
df_country.to_csv(r'.\Output\maldives.csv', index =False)
