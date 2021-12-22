#Import libraries
from pandas import read_csv, factorize,ExcelWriter
from numpy import where

#Read Data
df = read_csv(r".\2021\Week - 51\Input\Week-51_input.csv", parse_dates=['Order Date'],
              encoding='mbcs', dayfirst= True)


#Process Data
# Split OrderID details
df[['Store', 'OrderID']] = df['OrderID'].str.split('-', expand=True)
#Change Unit price to float
df['Unit Price'] = df['Unit Price'].str.strip('£').astype('float')
df['Sales'] = df['Unit Price']* df['Quantity']

#Return State
df['Returned'] = where(df['Return State'].isna(), 0, 1)

#Create IDs
cols = ['Store', 'Product Name', 'Customer']
for col in cols:
    df.sort_values(by=['Order Date', col], inplace= True)
    df[col+'ID'] = factorize(df[col])[0] + 1
df.rename(columns={'Product NameID': 'ProductID'}, inplace= True)

# Store dimension Table
store_tbl = df.groupby(['StoreID', 'Store']).agg(First_Order=('Order Date', 'min')).reset_index()

# Products dimension table
products_tbl = df.groupby(['ProductID', 'Category', 'Sub-Category', 'Unit Price',
    'Product Name'], as_index= False).agg(First_Order = ('Order Date','min'))

#customer dimension table
customer_tbl = df.groupby(['CustomerID', 'Customer'], as_index = False).agg(
                    Return_percent=('Returned', lambda x: sum(x)/len(x)),
                    Number_of_Orders=('Order Date', 'nunique'),
                    First_Order = ('Order Date', 'min'))

# Orders table
order_facts = df[['StoreID', 'CustomerID', 'OrderID', 'Order Date', 'ProductID','Returned',
                  'Quantity', 'Sales']]

#OUTPUT
dfs_dict ={'Order Facts': order_facts, 'Customers': customer_tbl, 
           'Products': products_tbl, 'Stores': store_tbl}
writer = ExcelWriter(r'.\2021\Week - 51\Output\week-51-Output.xlsx', engine='xlsxwriter')
for sheet, frame in dfs_dict.items():
    frame.to_excel(writer, sheet_name=sheet, index = False)
    
writer.save()
print('end')   
    


