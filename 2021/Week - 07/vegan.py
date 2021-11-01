#Import Libraries
import pandas as pd
import os


os.chdir(r'c:\Users\DIANA\Desktop\Prepping_data')

#READ DATA
sheet_names = ["Shopping List", "Keywords"]
xlsx = pd.read_excel(r"./Data/Shopping List and Ingredients.xlsx", sheet_name = sheet_names)
shopping = xlsx["Shopping List"]
keywords = xlsx["Keywords"]


#PROCESS DATA
#Add E to E numbers 
e_nos = keywords["E Numbers"].to_list()[0].split(",")
prohibited = ["E"+ e.strip() for e in e_nos]

#Add Animal ingridients to prohibited list
ingridients_lst = keywords.iloc[:, 0].to_list()[0].split(",")
ingridients_lst = [ing.strip() for ing in ingridients_lst]
prohibited.extend(ingridients_lst)

#Add the prohibited products to the shopping dataframe
shopping["prohibited"] = str(prohibited).strip("[").strip("]").replace("'", "")
shopping["Ingredients/Allergens"] = shopping["Ingredients/Allergens"].apply(lambda x : x.lower())

#Define a function to test if a prohibited ingridient is in product 
def vegan_test(row):
    
    lst = []
    #if row contains prohibited ingridients
    for p in prohibited:
        if p.lower() in row:
            lst.append(p)
        else:
            ""
    return lst

#Apply vegan test function
shopping["Vegan_or_Not"] = shopping.apply(lambda x: vegan_test(x["Ingredients/Allergens"][:]), axis= 1)

#Select Vegan Products
vegan = shopping[shopping["Vegan_or_Not"].str.len() == 0]
vegan = vegan[["Product", "Description"]]

#Select Non_vegan Products
non_vegan = shopping[shopping["Vegan_or_Not"].str.len() != 0]
non_vegan = non_vegan[["Product", "Description", "Vegan_or_Not"]]
non_vegan = non_vegan.rename(columns={"Vegan_or_Not": "Contains"})
non_vegan["Contains"] = non_vegan["Contains"].apply(lambda x: ", ".join(x) )

#SAVE OUTPUT
vegan.to_csv(r'./Output/vegan_lst.csv', index = False)
non_vegan.to_csv(r'./Output/non_vegan_lst.csv', index = False)