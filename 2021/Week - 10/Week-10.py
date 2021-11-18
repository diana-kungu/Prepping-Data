
#IMPORT MODULES
import pandas as pd
from numpy import where
import re


#READ DATA
with  pd.ExcelFile(r'.\Data\Pokemon Input.xlsx') as xl:
    evol = pd.read_excel(xl, 'Evolution')
    poke = pd.read_excel(xl, 'Pokemon')


#PROCESS DATA
#Filter Pokémon up to Generation III, #386 and below
poke['#'] = poke['#'].astype(float) #change # field to float
poke = poke[poke.loc[:,'#'] <= 386]

#remove Type field and retain one row per Pokémon
poke.drop_duplicates(subset=['#'], inplace= True)
poke.drop('Type', axis=1, inplace=True)
#Remove pokemon with Mega in their name
poke = poke[~poke.Name.str.strip().str.contains(r"^Mega\s", regex = True)] 

#Process evolution dataset
# _filter pokemon 386 and less from both evolving from and to fields
# - Drop duplicates
gen3 = list(poke.Name.values)
indx =[i for i in range(evol.shape[0]) if (evol['Evolving from'][i] in gen3) or
        (evol['Evolving to'][i] in gen3)]
evol = evol.iloc[indx, :].reset_index(drop=True)
#Drop duplicates
evol = evol.drop_duplicates(subset=['Evolving from', 'Evolving to'])

#Join pokemon data with evolution dateset
df_merged = pd.merge(poke, evol, how= 'left', left_on= 'Name', right_on= 'Evolving from')

#Create Evolving from field 
evol_dict_1 = dict(zip(evol['Evolving from'], evol['Evolving to']))
evol_dict_2 = dict(zip(evol['Evolving to'], evol['Evolving from']))
df_merged['Evolving from'] = [evol_dict_2.get(i) for i in df_merged['Name']]

# Evolution path
path = set()
def path_2(ele):
    path.add(ele)
    
    if ele in evol_dict_1.keys():
        if ele in evol_dict_2.keys():
            path.add(evol_dict_2[ele])

        ele = evol_dict_1.get(ele)
        path_2(ele)
       
    else:
         if evol_dict_2.get(ele) not in path:
            path.add(evol_dict_2.get(ele))
            ele = evol_dict_2.get(ele)
            path_2(ele)     
    return path.difference([None])
        
# 
all_paths = []
# Create evolutio path for each pokemon
for i in range(df_merged.shape[0]):
    path = set()
    ele = df_merged['Name'][i]
    path_2(ele)
    all_paths.append(list(path))


df_merged['Evolution Path'] = all_paths

# Eolution group: - first member of each group
evo_group = []

for i in range(df_merged.shape[0]):
    
    names = df_merged['Evolution Path'].iloc[i]
    x = pd.concat([df_merged[df_merged['Name']== n] for n in names])
    if len(x) >0:
        l = [x.Name.iloc[i]  for i in range(x.shape[0]) if (x.iloc[i, 9] is None) ]
        if len(l) ==0:
            evo_group.append(df_merged['Evolving from'].iloc[i])
            
        else:
            evo_group.append(l[0])
    else:
        evo_group.append(df_merged.Name.iloc[i])
        
df_merged['Evolution Group'] = evo_group

#Arrange columns 
col = df_merged.pop('Evolution Group')
df_merged.insert(0, 'Evolution Group', col)

#  Pokémon that have 3 evolutions, we want to know what the First Evolution is in their Evolution Group 
# Select pokemon with more than 2 evolutions
names = df_merged['Evolution Group'].values.tolist()
counts = set([x for x in names if names.count(x)>2 ]) 

df_merged['First Evolution'] = where((df_merged['Evolving to'].isna()) & (~df_merged['Evolving from'].isna()) &
                                (df_merged['Evolving from'] != df_merged['Evolution Group']), \
                                df_merged['Evolution Group'], "")

df_merged.drop('Evolution Path', axis= 1, inplace= True)


# Remove pokemons that evolve to class not in original pokemon data
dups_df = df_merged[df_merged.duplicated(subset=['Name', 'Evolving from'])]
[x for x in dups_df['Evolving to'].values if x not in poke.Name.values]
df_merged = df_merged[(df_merged['Evolving to'] != 'Gallade') & (df_merged['Evolving to'] != 'Froslass')]

# OUTPUT
df_merged.to_csv(r'.\Output\pokemon.csv', index= False)




