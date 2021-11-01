#Import Data
import pandas as pd
import zipfile
import os


#Read data 
cols = ['Name', 'Position', 'Appearances', 'Goals',
       'Headed goals', 'Goals with right foot', 'Goals with left foot', 'Penalties scored', 'Freekicks scored']
zf = zipfile.ZipFile('.\Data\Week 13.zip') 

_list_files = []
for text_file in zf.infolist():
    df= pd.read_csv(zf.open(text_file.filename), usecols=cols)
    _list_files.append(df)

pl = pd.concat(_list_files)


#PROCESS DATA
#Drop goalkeepers & Remove players with 0 Appearance
pl = pl[~(pl['Position'] == 'Goalkeeper') & (pl['Appearances'] != 0)]

#Fill NaNs and create Open play Goals and Open Goals/Game field
pl.fillna(0, inplace= True)
pl['Open Play Goals'] = pl['Goals'] - (pl['Penalties scored'] + pl['Freekicks scored'])
pl['Open Goals/Game'] = pl['Open Play Goals']/pl['Appearances']
#Rename a Column
pl = pl.rename(columns={'Goals': 'Total Goals'})
#Aggregate desired fields by Name and Postion
pl_grped = pl.groupby(['Name', 'Position'])['Open Play Goals', 'Headed goals', 'Goals with right foot',
                         'Goals with left foot', 'Appearances', 'Total Goals'].sum().reset_index()

#Create Overall Ranks and Ranks by Position fields
pl_grped['Rank'] = pl_grped['Open Play Goals'].rank(method='min', ascending =False).astype(int)
pl_grped.sort_values(by='Rank', inplace=True)
pl_grped['Rank by Position'] = pl_grped.groupby(['Position'])['Open Play Goals'].\
                rank(method='min', ascending =False).astype(int)
pl_grped.sort_values(by=['Rank by Position'], inplace=True)

#Top 20 players Overall
top_20 = pl_grped[pl_grped['Rank'] <= 20]
#Top 20 players for each Postion 
idx = [i for i in range(len(pl_grped)) if pl_grped['Rank by Position'].iloc[i] <= 20 ]
pl_ranked_position = pl_grped.iloc[idx, :]


#OUTPUT
top_20.to_csv(r'.\Output\top20_overall.csv', index = False)
pl_ranked_position.to_csv(r'.\Output\top20_by_postion.csv', index = False)


                    