[**Week 8**](https://preppindata.blogspot.com/2022/02/2022-week-8-pokemon-evolution-stats.html)

**Requirements**

- Import the data (excel file)
- From pkmn_stats dataset remove the columns height, weight and evolves from
- Pivot (wide to long) pkmn stats so that hp, attack, defense, special_attack, special_defense, and speed become a column called 'combat_factors'
- Using the evolutions data look up the combat_factors for each Pokémon at each stage, making sure that the     combat_factors match across the row, i.e. we should be able to see the hp for Bulbasaur, Ivysaur and Venusaur on one row
- Remove any columns for 'pokedex_number' and 'gen_introduced' that were from joins at Stage 2 & 3
- If a Pokémon doesn't evolve remove it from the dataset
- Find the combat power values relating to the Pokémon's last evolution stage
- Sum together each Pokémon's combat_factors
- Find the percentage increase in combat power from the first & last evolution stage
- Sort the dataset, ascending by percentage increase
- Output the data
