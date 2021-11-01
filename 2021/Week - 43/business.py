#IMPORTS
from pandas import read_excel, ExcelFile, to_datetime,concat
from os import chdir
from numpy import where

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#READ DATA
with ExcelFile(r'.\Data\2021W43 Input.xlsx') as xl:
    unit_A = read_excel(xl, 'Business Unit A ')
    unit_B = read_excel(xl, 'Business Unit B ', skiprows= 5)
    risk = read_excel(xl, 'Risk Level')

#PROCESS DATA
#Remove whitespaces and format date columns
unit_B['Date lodged'] = to_datetime(unit_B['Date lodged'], dayfirst= True)# format= '%d%m%Y')
unit_B.columns = [c.strip() for c in unit_B.columns]
unit_A.columns = [c.strip() for c in unit_A.columns] #Strip whitespace in column names    
#Create Date Lodged field
date_cols = ['Year', 'Month', 'Date']
unit_A[date_cols] = unit_A[date_cols].astype(str) 
unit_A['Date lodged'] = unit_A.apply(lambda row :to_datetime(row['Year']+row['Month']+ row['Date'],
                                   format ='%Y%m%d'), axis= 1)
unit_A.drop(date_cols, axis= 1, inplace= True)                                   
#Update risks ratings
unit_A['Rating'] = unit_A['Rating'].map({1:'Low', 2: 'Medium', 3: 'High'})
#Combine Units A and B
unit_A.rename(columns=({'Business Unit': 'Unit'}), inplace= True)
df = concat([unit_A, unit_B], ignore_index = True)
df_o = df.copy()

#Create Case Type field: Cases lodged before 2021-10-01 or after
df['Case Type'] =where(df['Date lodged'] < '2021-10-01', 'Opening Cases', 'New Cases')
df = df.drop('Status', axis=1)
df.rename(columns={'Case Type': 'Status'},inplace= True)
#Merge
result = concat([df, df_o])

#Agg by Status and Rating
result = result.groupby(['Status', 'Rating']).count().unstack(\
                    fill_value=0).stack().reset_index().sort_values(by= 'Rating')
result = result.iloc[:, 0:3]  
result.rename(columns= {'Ticket ID': 'Cases'}, inplace= True)                  
result['Status'] = result['Status'].replace({'In Progress': 'Continuing'})


#OUTPUT
result.to_csv(r'.\Output\w43_cases.csv', index= False)