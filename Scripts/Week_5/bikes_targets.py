#Import Libraries
import pandas as pd
import numpy as np
import os


# Read data

sheet_names = ["Manchester", "London", "Leeds", "York", "Birmingham", "Targets"]

xls_dict = pd.read_excel(r'.\Data\PD_2021_Wk.xlsx', sheet_name= sheet_names, parse_dates= True)

for location in sheet_names[:-1]:
    loc = xls_dict[location]

    #Add store location field to store based dataframe
    loc["Store"] = location

df = pd.concat([xls_dict['Manchester'], xls_dict['London'] , xls_dict['Leeds'],
                     xls_dict['York'], xls_dict['Birmingham']])
#Store Target data
targets = xls_dict['Targets']


#PROCESS DATA

#Change from wide to long format
df_melt = pd.melt(df,id_vars= ['Date', 'Store'], var_name = "Product-Customer", value_name= 'Products Sold')

#Create Quarter field
df_melt['Quarter'] = df_melt['Date'].dt.quarter
df_melt.drop('Date', axis=1, inplace= True)

#Groupby Quarter and Store
gpd_store_quarter = df_melt.groupby(["Quarter","Store"], as_index= True)['Products Sold'].sum().reset_index()

#Merge with Targets
targets_quarter_store = pd.merge(gpd_store_quarter, targets , 
            on=["Quarter", "Store"], how='left')

#Create Target to Variance field
targets_quarter_store["Variance to Target"] = targets_quarter_store["Products Sold"] - targets_quarter_store["Target"]

#Create Rank field
targets_quarter_store["Rank"] = targets_quarter_store.groupby("Quarter")["Variance to Target"].rank(ascending = False).astype('int')
   
#Reposition Rank field on the dataframe
col = targets_quarter_store.pop("Rank")
targets_quarter_store.insert(1, col.name, col)


#OUTPUT
targets_quarter_store.to_csv(r'./Output/target_quarter_store.csv', index = False)