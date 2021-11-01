import pandas as pd
import numpy as np
import os
import re
from datetime import datetime


#-------------------------------------------------------------------------------
#Read data
#-------------------------------------------------------------------------------

date_parser = lambda x : datetime.strptime(x , "%d/%m/%Y")
df = pd.read_csv(r'.\Data\Bikes_w2_2021.csv', parse_dates=['Order Date', 'Shipping Date'],
                                            date_parser = date_parser  )


#---------------------------------------------------------------------------------
#Process Data
#---------------------------------------------------------------------------------

#------------------Table One----------------------------------------------
#Retrive Model Code
df["Model"] = df.Model.str.findall('[A-Z]+').transform(''.join)

#Create Order Value field
df["Order Value"] = df.apply(lambda row: row["Quantity"]* row["Value per Bike"],
                                    axis = 1)   

#Pivot table by Model and Type with aggregate Quantity and Order Value
bike_sales =pd.pivot_table(df, index=["Model", "Bike Type"], values= ["Order Value", "Quantity"],
                          aggfunc= 'sum').reset_index()
bike_sales = bike_sales.rename(columns={"Quantity": "Quantity Sold"}) 

#Create average Bike Value by Model and Type field
bike_sales["Average Bike Value by Model and Type "] = (bike_sales["Order Value"]/ 
                                                            bike_sales["Quantity Sold"]).round(1)


#------------------Table Two----------------------------------------------

#Create Days to Ship Field
df["Days to Ship"] = (df['Shipping Date'] - df['Order Date']).dt.days

#Pivot table by Model and Store with aggregate Quantity, Days to Ship, and Order Value
bikes_ship = pd.pivot_table(df, index=["Model", "Store"], values= ["Order Value", "Quantity", "Days to Ship"],
                          aggfunc= {"Order Value":sum, "Quantity": sum, "Days to Ship": np.mean}).reset_index()
bikes_ship["Days to Ship"]= bikes_ship["Days to Ship"].round(1)


#-------------------------------------------------------------------------------
#Save output
#-------------------------------------------------------------------------------
bike_sales.to_csv(r'./Output/bikes_sale_model.csv', index= False)
bikes_ship.to_csv(r'./Output/bikes_store_ship.csv', index= False)
