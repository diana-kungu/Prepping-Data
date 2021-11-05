#IMPORTS
from pandas import ExcelFile, read_excel, concat
from os import chdir
from numpy import where, std, floor


#READ 
names = ['Airline', 'CustomerID', 'Score']
with ExcelFile(r'.\Data\NPS Input.xlsx') as xl:
    airlines = read_excel(xl, 'Airlines',  names= names)
    prep = read_excel(xl, 'Prep Air', names= names)

#PROCESS DATA
#Filter out airlines with less than 50 passengers
pass_per_airline = airlines.groupby('Airline')['CustomerID'].size(
         ).reset_index().rename(columns={'CustomerID': 'Total Passengers'})

small_airlines = pass_per_airline[pass_per_airline['Total Passengers'] < 50]
small_airlines = small_airlines.Airline.tolist()
airlines = airlines[~airlines['Airline'].isin(small_airlines)]

#Join 
df = concat([prep, airlines], ignore_index= True) 

# 
df['Customer Response'] = where(df['Score'] < 7, 'Detractors',
                                where(df['Score'] < 9, 'Passive', 'Promoters'))

# 
df = df.groupby(['Airline', 'Customer Response'])['CustomerID'].count().rename('Count').reset_index()
df = df.pivot(index= 'Airline', columns= 'Customer Response', values='Count').reset_index()

#Calculate % of Detractors, Passive, Promoters
df[['Detractors', 'Passive', 'Promoters']] = df[['Detractors', 'Passive', 'Promoters']].apply(
                                                    lambda x: floor(x*100/x.sum()), axis=1)
#Calculate NPS
df['NPS'] = df['Promoters'] - df['Detractors']

#Calculate Avg and Standard Deviation
Avg_nps, std = [df['NPS'].mean(),  df['NPS'].std()]

#calculate Z-score
df['Z-Score'] =  (df['NPS'] - Avg_nps)/std

#Filter out Prep Air
df[df['Airline'] == 'Prep Air']

# OUTPUT
df.to_csv(r'.\Output\week-23.csv', index= False)
                                
