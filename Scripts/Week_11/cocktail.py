import pandas as pd
import os


#READ DATA
with pd.ExcelFile(r".\Data\cocktails.xlsx") as xl:
    cocktail = pd.read_excel(xl, 'Cocktails')
    prices = pd.read_excel(xl, 'Sourcing')
    xchange_rates = pd.read_excel(xl, 'Conversion Rates')


#PROCESS DATA
#Split Ingredients lists
cocktail['Recipe (ml)'] = cocktail['Recipe (ml)'].str.split(';')

#Create ingredients Dict
recipe_lst =[]
for i in range(len(cocktail)):
    ing = {}
    for j in cocktail['Recipe (ml)'][i]:
        recipe = j.split(':')
        ing[recipe[0].strip()] =recipe[1][:-2]
    recipe_lst.append(ing)
cocktail['Recipe (ml)'] = recipe_lst

#price in pounds
prices[['Price', 'ml per Bottle']] = prices[['Price', 'ml per Bottle']].astype(float)
prices['Ingredient'] = prices['Ingredient'].str.strip()

#Create Exchange rate dictionary and map with the Sourcing data
xchange_dict =dict(zip(xchange_rates['Currency'], xchange_rates['Conversion Rate £']))
prices['Currency'] = prices['Currency'].map(xchange_dict)

#Create price per ml in £ field
prices['£/ml'] = prices.apply(lambda x : (x['Price'] / x['Currency'])/x['ml per Bottle'], axis=1)

#Create Price dict
price_dict = dict(zip(prices['Ingredient'], prices['£/ml']))

#Create Cost, Margin fields
cocktail["Cost"]= [sum([(int(cocktail['Recipe (ml)'][i][key]))*price_dict[key]
                        for key in cocktail['Recipe (ml)'][i].keys()]) for i in range(len(cocktail))]
cocktail["Margin"] = cocktail['Price (£)'] - cocktail['Cost']

#Format fields and drop unwanted columns
cocktail.drop('Recipe (ml)', axis=1, inplace= True)
cocktail[['Cost', 'Margin']] = cocktail[['Cost', 'Margin']].round(2)

#SAVE OUTPUT
cocktail.to_csv(r'.\Output\cocktail.csv', index = False)
