#Import Libraries
import pandas as pd
import numpy as np
import os


print(os.getcwd())

#READ DATA
data = pd.read_excel(r'./Data/PGALPGAMoney2019.xlsx')
data.columns = [col.lower().title() for col in data.columns]


#PROCESS DATA
#Create Avg. Prize Money per player field
data['Avg. Money per Player']= (data['Money']/ data['Events']).astype('int')

#Create Ranks fields; Overall, Tour & Rank Diff
data['overall_rank'] = data['Money'].rank(method= 'first', ascending=False)
data['tour_rank'] = data.groupby("Tour")['Money'].rank(method= 'first', ascending=False)
data['Rank Diff'] = (data['overall_rank'] - data['tour_rank']).round(2)

#Groupby Tour
grouped = data.groupby("Tour").agg({"Money": 'sum', "Events": 'count',
                    "Player Name": 'count','Events': 'sum', 'Avg. Money per Player': 'mean',
                    'Rank Diff': 'mean'}).reset_index()

#Rename columns
grouped.columns = ['Tour','Total Prize Money','Number of Events', 'Number of Players',
                    'Avg Money per Event', 'Avg Difference in Ranking']

#Melt the dataframe
melted = grouped.melt(id_vars="Tour", var_name= "Measures")

#Pivot the melted dataframe 
df_final = melted.pivot(index = "Measures", columns= "Tour", values= "value").reset_index()

#Create Difference between Tours field
df_final["Difference between tours"] = (df_final['PGA']) - (df_final["LPGA"])

#Format the numeric values
df_final.iloc[0, 1:] = df_final.iloc[0, 1:].apply(lambda x : '{:,.2f}'.format(x))
df_final.iloc[1:, 1:] = df_final.iloc[1:, 1:].applymap(lambda x : '{:,}'.format(int(float(x))))


#OUTPUT
df_final.to_csv(r'./Output/pga_lpga.csv', index= False)


