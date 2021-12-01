# Import Libraries
from pandas import ExcelFile, read_excel, Series, pivot_table, merge
from numpy import mean, where

# Read Data
with ExcelFile(r'.\2021\Week - 36\Input\Input\Trend Input.xlsx') as xl :
    trend = read_excel(xl, sheet_name = 'Timeline', skiprows=2)
    country = read_excel(xl, sheet_name = 'Country Breakdown', skiprows=2 )

#Process data
#Clean column names
trend.columns = [c.replace(': (Worldwide)', '') for c in trend.columns]

#Calculate Overall Average Index
trend = trend.melt(id_vars ='Week', var_name = 'Search Term', value_name='Index' )
summary = trend.groupby(['Search Term']).agg(
        Avg_Index =('Index', 'mean'),
        First_Peek =('Index' ,'idxmax')).reset_index()

#First time search term peeked(100)
summary['First_Peek'] = trend.iloc[summary.First_Peek]['Week'].values

# For each year (1st September - 31st August), calculate the average index
trend['C_Y'] = trend.Week.dt.year
trend['year'] = where(trend.Week.dt.month >8, trend['C_Y'].astype('str')+'/'+
                (trend['C_Y'] +1).astype('str'),
                (trend['C_Y'] -1).astype('str')+'/'+trend['C_Y'].astype('str')
                )
yearly_trends = trend.groupby(['Search Term','year'], as_index = False)['Index'].mean(
                    ).rename(columns={'Index':'yearly_avg'})                      

yearly_trends = yearly_trends.iloc[where(yearly_trends['year'].isin(
                                        ['2019/2020', '2020/2021']))]
#Pivot
yearly_trends = pivot_table(yearly_trends, 'yearly_avg', 'Search Term', 'year', 'first').reset_index()
yearly_trends['Status'] = where(yearly_trends['2020/2021'] >
                                yearly_trends['2019/2020'], 'Still trendy', 'Lockdown Fad')
yearly_trends.drop('2019/2020', axis =1, inplace=True)

# For each search term, work out which country has the highest percentage
# Filter out countries with missing Indexes
country.dropna(how='any', inplace=True)
country.columns = ['Country', 'Pet adoption', 'Online streamer', 'Staycation']
country = country.melt(id_vars ='Country', var_name = 'Search Term', value_name='Index' )

country = country.set_index('Country').groupby(['Search Term']).agg(
    Country_with_highest_percentage=('Index', 'idxmax')).reset_index()


summary= merge(summary, yearly_trends, how='left').merge(
                    country, how='left')
#output columns
summary.rename(columns= {'2020/2021': '2020/2021 Avg Index'}, inplace= True)
summary[['Avg_Index', '2020/2021 Avg Index']] = summary[['Avg_Index', '2020/2021 Avg Index']]. round(2)
summary.columns = [c.replace('_', ' ') for c in summary.columns]

#OUTPUT
summary.to_csv(r'.\2021\Week - 36\Output\week-36-output.csv', index=False)
print('End')


