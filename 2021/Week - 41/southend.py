import pandas as pd
import os
import re

#os.chdir('..')

#READ DATA
df = pd.read_csv(r".\Data\southend.csv")
pattern = re.compile(r'(?P<Season>\d+\-\d+)\s+(?P<League>\w+\-\w+)\s+(?P<P>\d+)\s+(?P<W>\d+)\s+(?P<D>\d+)\s+(?P<L>\d+)\s+(?P<F>\d+)\s+(?P<A>\d+)\s+(?P<Pts>\d+)\s+(?P<Pos>\d+\/\d+|\w+)')

#Extract data from string
southend = df.iloc[:,0].str.extract(pattern)
southend.dropna(axis=0, how='all', inplace= True)

#PROCESS DATA
#Find missing seasons and include in the dataframe
first = int(southend["Season"][0][:4])
end = int(southend["Season"].iloc[-1][:4])+ 1

missing_seasons = [(str(i)+"-"+ str(i+1)[-2:])  for i in range(first, end+1) 
        if  (str(i)+"-"+ str(i+1)[-2:]) not in southend.Season.to_list() ]

for item in (missing_seasons):
    row = [" "]*9
    row.insert(0, item)
    southend = southend.append(pd.Series(row, index=southend.columns), ignore_index = True)
southend.sort_values(by="Season", inplace= True)

#Create Special Circumstances field
southend['Special Circumstances'] = southend.apply(lambda x : "WW1" if x["Season"] in missing_seasons[:4] 
                                    else "WW2" if x["Season"] in missing_seasons[4:-1] 
                                    else "Incomplete" if x["Season"] == '2021-22'
                                    else 'N/A', axis = 1)

#Fix 1939-40/2021-22 season
southend.loc[southend['Season'] == '1939-40', ['Special Circumstances', 'Pos']] = ["Abandoned Due to WW2", ""]
southend.loc[southend['Season'] == '2021-22', ['League']] = "NAT-P"

#Extract League Numeric 
southend["League No"] = southend["League"].apply(lambda x : 0 if x == "FL-CH" else 5 if x == 'NAT-P' else x[-2] if x.endswith("S") else x[-1])
southend["League No"] = pd.to_numeric(southend["League No"], errors= 'coerce')
southend['No.shift'] = southend['League No'].shift(-1)

#Create Outcome Field;- Same League, promoted or relegated
southend['Outcome'] = southend.apply(lambda x : "Same League" if x["League No"] == x['No.shift'] else "Promoted" 
                                if x["League No"] > x['No.shift'] else "Relegated" if x["League No"] < x['No.shift'] 
                                else "N/A" , axis= 1)

southend.drop(["League No", "No.shift"], axis= 1, inplace= True)

#Clean index & rearrange column 
col_index = [0,11,10,1,2,3,4,5,6,7,8,9]
southend = southend[[southend.columns[i] for i in col_index]]

southend.reset_index(drop = True,inplace=True)


#OUTPUT
southend.to_csv(r'./Output/southend.csv', index = False)

