#Import Libraries
import pandas as pd
import numpy as np
import os


#Read data
df = pd.read_csv(r'.\Data\duplicates.csv', parse_dates= ['From Date'], dayfirst= True )


#PROCESS DATA
#Group by Client
grouped = df.groupby(["Client"])

#Extract row index for max date per group
max_date_idx = []

for name, group in grouped:
    max_date_idx.append(group['From Date'].idxmax())

#Recent Clients IDs and Account Managers dataframe
recent_acc_managers = df.iloc[max_date_idx, -4:]

#Update all records with recent records details
update_df = pd.merge(df, recent_acc_managers,how='left', on =['Client'], suffixes=["_old", ""])
update_df.drop(update_df.columns[[4,5,6]], axis= 1, inplace= True)

clean_df = update_df.drop_duplicates(keep='first')

#SAVE OUTPUT
clean_df.to_csv(r".\Output\cleaned_duplicate.csv", index= False)
