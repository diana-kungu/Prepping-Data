#Import libraries
import pandas as pd
import numpy as np
import os


#-------------------------------------------------------------------------------------
#Read data
#-------------------------------------------------------------------------------------
bikes = pd.read_csv(r'.\Data\Bikes_w1_2021.csv', parse_dates = ["Date"])


#--------------------------------------------------------------------------------------
#Process Data
#--------------------------------------------------------------------------------------

#Split Store-Bike field and drop Store -Bike field
bikes[['Store', "Bike"]] = bikes["Store - Bike"].str.split("-", expand = True)
bikes.drop("Store - Bike", axis = 1, inplace = True)

#Clean Bike field
bikes = bikes.replace(to_replace = "^ R.*d$", value = "Road", regex = True)
bikes = bikes.replace(to_replace = "^ M.*", value = "Mountain", regex = True)
bikes = bikes.replace(to_replace = "^ G.*", value = "Gravel", regex = True)

#Create Quarter and Day of Month fields for each Date
bikes["Quarter"] = bikes.Date.dt.quarter
bikes["Day of Month"] = bikes.Date.dt.day

#Drop Date field
bikes.drop("Date", axis = 1, inplace = True)

#Remove first 10 rows of test data
bikes_output = bikes.iloc[10:]


#--------------------------------------------------------------------------------
#Save output
#---------------------------------------------------------------------------------
bikes_output.to_csv(r'./Output/bikes_output.csv', index = False)




