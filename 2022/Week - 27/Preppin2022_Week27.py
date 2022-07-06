
#Load Libraries
from pandas import read_csv

#read data
df = read_csv(r".\2022\Week - 27\Input\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv")


# Processing
#Separate out the Product Name field to form Product Type and Quantity
#Rename the fields to 'Product Type' and 'Quantity' respectively
df[['Product Type','Quantity']] = df['Product Name'].str.split(' - ', expand= True)

#Clean the Quantity field to just leave values 
# For Liquid, ensure every value is in millilitres 
df['Quantity'] = df['Quantity'].str.replace('1L', '1000ml')
df['Quantity'] = df['Quantity'].str.extract('(\d+)').astype('int')

#count the number of orders that has the combination of Store, Region and Quantity.
df['Present in N orders'] = (df.groupby(['Store Name', 'Region', 'Quantity', 'Product Type'])
                             ['Order ID'].transform('nunique'))

# Sum up the sales for each combination of Store, Region and Quantity
liquid_sales = df[df['Product Type'] == 'Liquid'].groupby(['Store Name', 'Region', 'Quantity', 
                                            'Present in N orders'])['Sale Value'].sum().reset_index()
bar_sales = df[df['Product Type'] == 'Bar'].groupby(['Store Name', 'Region', 'Quantity', 
                                            'Present in N orders'])['Sale Value'].sum().reset_index()

#OUTPUT
liquid_sales.to_csv(r'.\2022\Week - 27\Output\liquid_sales.csv', index = False)
bar_sales.to_csv(r'.\2022\Week - 27\Output\bar_sales.csv', index = False)


