
#Import 
from pandas import read_csv
from datetime import datetime as dt
from numpy import timedelta64, where
from math import floor, ceil

# Normal half way round function
def normal_round(n):
    if n - floor(n) < 0.5:
        return floor(n)
    return ceil(n)


#Read Data
df =read_csv(r'.\2021\Week - 49\Input\Week-49-Input.csv', parse_dates=['Date'], dayfirst= True)


# Process Data
df['Monthly Salary'] = df['Annual Salary'].apply(lambda x: round(x/12, 2))

employment_range = lambda x: x.min().strftime('%b %Y') +' to '+ x.max().strftime('%b %Y') 
df['Employment Range'] = df.groupby('Name')['Date'].transform(employment_range)

# Reporting year
df['Start Date'] = df.groupby('Name').Date.transform('min')
df['End Date'] = df.groupby('Name').Date.transform('max')
df['Reporting Year'] = df['Date'].apply(lambda x: x.strftime('%Y'))

#Calculate tenure
df['temp'] = df['Reporting Year'] +'/12/01'
df['temp'] = df.temp.apply(lambda x: dt.strptime(x,'%Y/%m/%d'))
df['End Date'] =[x if int(dt.strftime(y, '%Y')) < int(dt.strftime(z, '%Y')) else y
              for x,y,z in zip(df['temp'], df['Date'], df['End Date'])]
df['Tenure'] = ((df['End Date']- df['Start Date'])/timedelta64(1, 'M')) +1
df['Tenure'] = df['Tenure'].apply(normal_round)

'''Work out for each year employed per person:
    Number of months they worked
    Their salary they will have received 
    Their sales total for the year'''
df = df.groupby(['Name', 'Reporting Year']).agg(
                                        employment_range = ('Employment Range', 'first'),
                                        tenure =('Tenure', 'mean'),
                                        Salary_paid =('Monthly Salary', 'sum'),
                                        yearly_bonus =('Sales', lambda x: sum(x)*0.05)
                                        
                                        ).reset_index()
df['Total Earned'] = df['Salary_paid'] + df['yearly_bonus']


#OUTPUT
df.to_csv(r'.\2021\Week - 49\Output\Week-49-output.csv', index=False)
print('End')


