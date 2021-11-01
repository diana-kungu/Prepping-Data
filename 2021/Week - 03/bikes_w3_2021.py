#Import Libraries
import pandas as pd
import numpy as np
import os
from datetime import datetime


# READ DATA

sheet_names = ["Manchester", "London", "Leeds", "York", "Birmingham"]

xls_dict = pd.read_excel(r'.\Data\PD_2021_Wk.xlsx', sheet_name= sheet_names, parse_dates= True)

for location in sheet_names:
    loc = xls_dict[location]
    #Add store location field 
    loc["Store"] = location

df = pd.concat([xls_dict['Manchester'], xls_dict['London'] , xls_dict['Leeds'],
                     xls_dict['York'], xls_dict['Birmingham']])


#PROCESS DATA

#Melt the dataframe
df_melt = pd.melt(df,id_vars= ['Date', 'Store'], var_name = "Product-Customer", value_name= 'Products Sold')

#Create two fields Customer Type and Product
df_melt[['Customer Type','Product']] = df_melt['Product-Customer'].str.split("-", expand = True)
df_melt.drop('Product-Customer', axis=1, inplace= True)

#Create Quarter field from Date
df_melt['Quarter'] = df_melt['Date'].dt.quarter
df_melt.drop('Date', axis=1, inplace= True)


#Aggregation

#Groupby product and quarter
gpd_product_quarter = df_melt.groupby(['Product', "Quarter"], as_index= True)['Products Sold'].sum().reset_index()

#Groupby Store, customer Type, Product
gpd_store_customer_product = df_melt.groupby(['Store', 'Customer Type', 'Product'], as_index= True)['Products Sold'].sum().reset_index()


#SAVE OUTPUT
gpd_product_quarter.to_csv(r'./Output/bikes_product_quarter.csv', index = False)
gpd_store_customer_product.to_csv(r'./Output/bikes_store_customer_product.csv', index = False)
 