# Imports
from pandas import ExcelFile, read_excel, concat, to_datetime
from os import chdir
from datetime import datetime as dt
from numpy import where

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')


#...........................................................................................
#PROCESS DATA

#Read Data / Combine all sheets and create a column with sheet name
workbook  = ExcelFile(r'.\Data\PD_2021_Wk_21.xlsx')
sheets = workbook.sheet_names
df = concat([read_excel(workbook, sheet_name=s )
            .assign(Month = int(s.split()[1])) for s in sheets], ignore_index= True)

df['Destination'] = df['Destination'].str.strip()

#Use sheet name (Month) and Day of Month fields to make Date
df['Date'] = df.apply(lambda x: dt.strptime(f"2021-{x.Month}-{x['Day of Month']}",
                    '%Y-%m-%d'), axis = 1)

#Create New Trolley Inventory field to show whether the purchase
# was made on or after 1st June 2021
df['New Trolley Inventory?'] = where(df['Date'] > '2021-06-01', 'True', 'False' ) 

# Parse Product Name(return any names before the '-' (hyphen)
#If a product doesn't have a hyphen return the full product name)
df['Product'] = df['Product'].apply(lambda x:  x.split('-')[0].strip() if ('-') in x.strip() else x)

#Make price a numeric field
df['Price'] = df["Price"].apply(lambda x: float(x[1:]))

#Work out the average selling price per product
df['Avg Price per Product'] = df.groupby('Product')['Price'].transform('mean')

#Workout the Variance (difference) between the selling price and the average selling price
df['Variance'] = df['Price'] - df['Avg Price per Product']

#Rank the Variances (1 being the largest positive variance) per destination and New Trolley Inventory?
df['Rank'] = df.groupby(['Destination', 'New Trolley Inventory?'])['Variance']\
                        .rank('dense', ascending= False).astype('int')
df.sort_values(by = 'Rank', inplace = True)

#Return only ranks 1-5
top_5 = df[df['Rank'] < 6]


#..........................................................................................
#OUTPUT
top_5.to_csv(R'.\Output\week_21.csv', index= False)
