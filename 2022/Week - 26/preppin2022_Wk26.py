
#Load libraries
from pandas import read_csv, pivot_table

#Load Data
df = read_csv(r'.\2022\Week - 26\Input\Spotify Data Unclean.csv', usecols=['Artist Name', 'ms_played', 'ts'],
              parse_dates=['ts'])


#Extract the year from the timestamp field
df['Year'] = df['ts'].dt.year
#Total duration per artist
df['total ms_played'] = df.groupby('Artist Name').ms_played.transform(sum)

#Rank the artists by total minutes played overall
df['Overall Rank'] = df['total ms_played'].transform('rank', method = 'dense', ascending = False).astype('int')

# Reshape the data so we can compare how artist position changes year to year
df = pivot_table(df, 'ms_played', index= ['Overall Rank', 'Artist Name'], 
                 columns = 'Year', aggfunc= (sum)).reset_index()
# For each year, find the ranking of the artists by total minutes played
df = df.set_index(['Artist Name', 'Overall Rank']).rank(method = 'max', ascending = False).reset_index()
#Fill NAs
subset = [c for c in df.columns if isinstance(c, int) ]
df.loc[:, subset] = df.loc[:, subset].fillna('')

#Filter to the overall top 100 artists
df = df[df['Overall Rank']<101]

# OUTPUT
df.to_csv(r'.\2022\Week - 26\Output\week 26 output.csv', index= False)






