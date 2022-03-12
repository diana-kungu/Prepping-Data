# Load Libraries
from pandas import read_csv, Series, merge
from numpy import where, diff


#READ DATA
df = read_csv(r'.\2022\Week - 9\\Input\Superstore - Order.csv', parse_dates=['Order Date', 'Ship Date'])

#PROCESS DATA
#Order year 
df['Year'] = df['Order Date'].dt.year
#Find the year of first purchase for each customer
df['First Purchase']  = df.groupby(['Customer ID'])['Year'].transform('min')

# 
current_yr = df['Year'].max()

for key, group in df.groupby('Customer ID'):
    for yr in range(group['First Purchase'].iloc[0], current_yr+1):
        if yr not in group['Year'].values:
            df = df.append({'Year': yr, 'Customer ID': group['Customer ID'].iloc[0],
                            'First Purchase': group['First Purchase'].min()}, ignore_index=True)

#Create a field which flags whether a customer placed an order in a given year or not
df['Order?'] = where(df['Row ID'].isna(), 0,1)

#Create a field which flags whether or not a customer placed an order in the previous year
df['Prev_Value'] = (df.groupby(['Customer ID'])['Order?'].transform(lambda x: x.shift()))

'''classify the customers as follows:
    New = this is the first year the customer has ordered
    Consistent = the customer ordered this year and last year
    Sleeping = the customer has ordered in the past, but not this year
    Returning = the customer did not order last year, but has ordered this year '''
    
df['Customer Classification'] = where(df['Prev_Value'].isna(), 'New',
                                where((df['Order?']==1) & (df['Prev_Value'] == 1), 'Consistent',
                                where((df['Order?']==1) & (df['Prev_Value'] == 0),  'Returning',
                                      'Sleeping'          
                                            )))

# 2018 Cohort: count number of purchases per year for the 2018 cohort
cohort_18 = df[(df['First Purchase'] == 2018)].groupby(['Year'], as_index= False).apply(lambda x: Series({
    'YoY Difference': x[x['Order?'] == 1]['Customer ID'].nunique()}))
cohort_18['YoY Difference'] = cohort_18['YoY Difference'].rolling(window=2).apply(diff)

df = df.merge(cohort_18)

#OUTPUT
df.to_csv(r'.\2022\Week - 9\Output\week-9-output.csv', index = False)
print('End')
