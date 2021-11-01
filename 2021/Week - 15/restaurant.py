#Import
from pandas import ExcelFile, read_excel, concat
from os import chdir
from numpy import where

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#Read Data
with ExcelFile(r".\Data\Menu and Orders.xlsx") as xl:
    orders = read_excel(xl, 'Order', parse_dates=['Order Date'])
    menu = read_excel(xl, 'MENU')

#PROCESS DATA
# Split Menu Table by type of food
#Pizza
pizza = menu.iloc[:, 0:3]
pizza['Type'] = 'Pizza'
cols_names = ['Name', 'Price', 'ID', 'Type']
pizza.columns = cols_names
#Pasta
pasta = menu.iloc[:, 3:6]
pasta['Type'] = 'Pasta'
pasta.dropna(how= 'any', inplace= True)
pasta.columns = cols_names
#House Plates
plates = menu.iloc[:, 6:]
plates['Type'] = 'House Plates'
plates.dropna(how= 'any', inplace= True)
plates.columns = cols_names
plates
#Concat Pizza, Pasta and House plates df to create new menu
menu = concat([pizza, pasta, plates], ignore_index= True)
menu['ID'] = menu['ID'].astype(int)

#Each Order on separate row
orders['Order'] = orders['Order'].apply(lambda x: x.split('-') if len(str(x)) >5 else x)
orders = orders.explode('Order')
orders['Order'] = orders['Order'].astype(int)

#Combine menu and orders dfs
combine = orders.merge(menu, how= 'left', right_on= 'ID', left_on='Order')
#Create Weekday field
combine['Weekday'] = combine['Order Date'].dt.day_name()
#Apply the Monday discount
combine['Price'] = where(combine['Weekday'] == 'Monday',\
                        combine['Price'] * 0.5, combine['Price'])

#Total by Weekday
total_weekday = combine.groupby('Weekday')['Price'].sum().reset_index()\
                            .sort_values(by='Price', ascending = False)
total_weekday.Price = total_weekday.Price.astype(int)

#Top customer by items ordered
items_order = combine.value_counts(subset=['Customer Name']).to_frame().reset_index()
top_customer = items_order.iloc[[0]]
top_customer.rename(columns={0: 'Count Items'}, inplace= True)


#OUTPUT
total_weekday.to_csv(r'.\Output\total_by_weekday.csv', index = False)
top_customer.to_csv(r'.\Output\top_customer.csv', index = False)