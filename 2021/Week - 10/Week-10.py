# %%
import pandas as pd
from numpy import where
import os
import re

# %%
os.chdir(r'C:\Users\DIANA\Desktop\Prepping_data')
os.getcwd()

# %%
with  pd.ExcelFile(r'.\Data\Pokemon Input.xlsx') as xl:
    evol = pd.read_excel(xl, 'Evolution')
    poke = pd.read_excel(xl, 'Pokemon')

# %%
poke.head()

# %%
#Filter Pokémon up to Generation III, #386
poke['#'] = poke['#'].astype(float) #change # field to float
poke = poke[poke.loc[:,'#'] <= 386]

#remove Type field and retain one row per Pokémon
poke.drop_duplicates(subset=['#'], inplace= True)
poke.drop('Type', axis=1, inplace=True)
poke
#g4_higher_names


# %%
#Remove pokemon with Mega in their name
poke = poke[~poke.Name.str.strip().str.contains(r"^Mega\s", regex = True)] # does not conatin mega in Name
poke

# %%
poke[poke['Name'] == 'Chimecho']

# %%
evol[evol['Evolving to'] == 'Chimecho']

# %%
#Process evolution data
# _filter pokemon 384 and less
# - remove 
# - Drop duplicates

gen3 = list(poke.Name.values)
indx =[i for i in range(evol.shape[0]) if (evol['Evolving from'][i] in gen3) and
    (evol['Evolving to'][i] in gen3)]

# %%
evol = evol.iloc[indx, :].reset_index(drop=True)
#Drop duplicates
evol = evol.drop_duplicates()

# %%
evol['Evolving from'] = evol['Evolving from'].str.strip()
evol['Evolving to'] = evol['Evolving to'].str.strip()


# %%
#Evolve to
df_merged = pd.merge(poke, evol, how= 'left', left_on= 'Name', right_on= 'Evolving from')
df_merged

# %%
evol_dict_1 = dict(zip(evol['Evolving from'], evol['Evolving to']))
evol_dict_2 = dict(zip(evol['Evolving to'], evol['Evolving from']))
evol_dict_2

# %%
df_merged['Evolving from'] = [evol_dict_2.get(i) for i in df_merged['Name']]
df_merged['Evolving to'] = [evol_dict_1.get(i) for i in df_merged['Name']]
df_merged

# %% [markdown]
# def get_evo_paths(row):
# 
#     ele = row['Name']
#     path = [ele]
#     #print(path)
#     
#     #for name in pokemon.Name.to_list():
#     def path_(ele):
#         
#         if ele in evol_dict_1.keys():
#             path.append(evol_dict_1[ele])
#             ele = evol_dict_1.get(ele)
#             
# 
#             path_(ele)
# 
#     return path
# 

# %%
path = set()
def path_(ele):
    
    path.add(ele)
        
    if ele in evol_dict_1.keys():
        #print(f'This is the current element {ele}')
        if ele in evol_dict_2.keys():
            #print(f'do a backward check for element {evol_dict_2[ele]}')
            path.add(evol_dict_2[ele])
            #print(f'The updated path is {path}')
        ele = evol_dict_1.get(ele)
        path_(ele)
                
    return path#evo_path
path_('Ivysaur')
        

# %%
path = set()
def path_2(ele):
    
    path.add(ele)
    #print(path)
    #if ele in evol_dict_2.keys()
        
    if ele in evol_dict_1.keys():
        #print(f'This is the current element {ele}')
        if ele in evol_dict_2.keys():
            #print(f'do a backward check for element {evol_dict_2[ele]}')
            path.add(evol_dict_2[ele])
            #print(f'The updated path is {path}')
        ele = evol_dict_1.get(ele)
        path_(ele)
        ''' print(f'This is the current element {ele}')
        if evol_dict_1.get(ele) not in path:
            path.add(evol_dict_1[ele])
            print(f'The updated path is {path}')
            ele = evol_dict_1.get(ele)
            path_(ele)
    if ele in evol_dict_1.values():
        if evol_dict_2.get(ele) not in path:
            path.add(evol_dict_2.get(ele))
            print(f'The updated path is {path}')
            ele = evol_dict_2.get(ele)
            path_(ele)'''
            #path.add(evol_dict_2[ele])
            
    else:# ele in evol_dict_1.values() and ele not in evol_dict_1.keys():
         if evol_dict_2.get(ele) not in path:
            path.add(evol_dict_2.get(ele))
            #print(f'The updated path is {path}')
            ele = evol_dict_2.get(ele)
            path_(ele)     
    return path.difference([None])
        


# %%
all_paths = []
for i in range(df_merged.shape[0]):
    path = set()
    ele = df_merged['Name'][i]
    path_2(ele)
    all_paths.append(list(path))


df_merged['Evolution Path'] = all_paths

# %%
df_merged['Evolution Path'] = df_merged['Evolution Path'].apply(lambda x:\
                        list(set(x).difference([None])))
df_merged.head(2)

# %%
evo_group = []

for i in range(df_merged.shape[0]):
    for n in df_merged['Evolution Path'].iloc[i]:
        x = df_merged[df_merged['Name']== n]
        #print(f' the name is {n}')
        if pd.isna(x.iloc[0, 9]):
            evo_group.append(n)

        


# %%
df_merged.iloc[369:375, :]

# %%
df_merged[df_merged['Evolution Path'].str.len() == 2]

# %%
df_merged[df_merged['Name'] == 'Fearow']

# %%
df_merged['Evolution Group'] = evo_group
df_merged

# %%
col = df_merged.pop('Evolution Group')
df_merged.insert(0, 'Evolution Group', col)
df_merged

# %%
names = df_merged['Evolution Group'].values.tolist()
counts = set([x for x in names if names.count(x)>2 ])


# %%
df_merged['First Evolution'] = where(df_merged['Evolution Group'].isin(counts) & 
                                df_merged['Evolving to'].isna(), \
                                df_merged['Evolution Group'], "")


# %%
df_merged

# %%
df_merged.drop('Evolution Path', axis= 1, inplace= True)
df_merged

# %%
#df_merged.to_csv('pokemon.csv', index= False)

# %%
output =  pd.read_excel(r'C:\Users\DIANA\Desktop\Prepping_data\Pokemon_week10_output.xlsx')
output.equals(df_merged) 

# %%
evol[evol['Evolving to'] == 'Chimecho']


