# Week 8
#Load modules
from pandas import ExcelFile, read_excel, melt
from numpy import where


#Read Data
with ExcelFile(r'.\2022\Week - 8\Input\input_pkmn_stats_and_evolutions.xlsx') as  xl:
    pkmn_stats = read_excel(xl, sheet_name = 'pkmn_stats')
    pkmn_evolutions = read_excel(xl, sheet_name = 'pkmn_evolutions')

# PROCESS DATA
#Remove the columns height, weight and evolves_from
pkmn_stats.drop(['height', 'weight', 'evolves_from'], axis=1, inplace= True)

#Pivot (wide to long) pkmn stats so that hp, attack, defense, special_attack, special_defense, 
# and speed become a column called 'combat_factors'
id_cols = ['name', 'pokedex_number', 'gen_introduced',]
pkmn_stats = (pkmn_stats.melt(id_vars = id_cols, var_name = 'combat_factors', value_name= 'score')
                .groupby(id_cols)['score'].sum().reset_index())

# remove pokemons that don't evolve from the dataset
pkmn_evolutions.dropna(thresh=2, inplace= True)

#look up the combat_factors for each Pokémon at each stage, making sure that 
# the combat_factors match across the row, i.e. we should be able to see the hp for 
# Bulbasaur, Ivysaur and Venusaur on one row
df = (pkmn_evolutions.merge(pkmn_stats, how= 'left', left_on='Stage_1', right_on='name')
      .drop('name', axis=1).rename(columns={'score': 'initial_combat_power'})
      .merge(pkmn_stats[['name', 'score']], how= 'left', left_on='Stage_2', right_on='name')
      .drop('name', axis=1).rename(columns={'score': 'stage_2_combat_power'})
      .merge(pkmn_stats[['name', 'score']], how= 'left', left_on='Stage_3', right_on='name')
      .drop('name', axis=1).rename(columns={'score': 'stage_3_combat_power'})
      )

# obtain final_combat_power from either stage_2 or stage_3
df['final_combat_power'] = where(df['Stage_3'].isna(), df['stage_2_combat_power'],
                                 df['stage_3_combat_power'])

#Find the percentage increase in combat power from the first & last evolution stage
df['combat_power_increase'] = ((df['final_combat_power'] - df['initial_combat_power'])
                               /df['initial_combat_power'])
df.sort_values('combat_power_increase', inplace= True)


# Output
output_cols = [col for col in df.columns if col != 'stage_2_combat_power' 
               or col != 'stage_2_combat_power'df.columns]
df.to_csv(r'.\2022\Week - 8\Output\pokemon_w8.csv', columns= output_cols, index= False)


