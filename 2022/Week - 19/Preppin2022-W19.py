
#Load modules
from pandas import ExcelFile, read_excel, merge

#Read  data
with ExcelFile(r'.\2022\Week - 19\Input\PD 2022 Wk 19 Input.xlsx') as xl :
    df = read_excel(xl, sheet_name = 'Product Set')
    sales = read_excel(xl, sheet_name = 'Sales' )
    sizes = read_excel(xl, sheet_name = 'Size Table')

# Process 
#Clean Product codes
df['Product Code'] = df['Product Code'].str.replace('S', '')\
#Change the Size ID to an actual Size value in the Sales table
sales = (sales.merge(sizes, left_on='Size', right_on= 'Size ID',
                     suffixes=("_Recorded", "")).drop('Size ID', axis= 1))
#Link the Product Code to the Sales Table to provide the Scent information
sales = (sales.merge(df, how='left', left_on='Product', right_on= 'Product Code',
             suffixes=('_Value_Recorded', '_Value')))

#Output 1
# Create an Output that contains the products sold that have the sizes recorded correctly 
correct_sizes = sales[sales['Size_Value_Recorded'] == sales['Size_Value']]
correct_sizes = correct_sizes[['Size_Value', 'Product', 'Store', 'Scent']]

#Output 2
#Incorrect records
incorrect = (sales[~(sales['Size_Value_Recorded'] == sales['Size_Value'])]
                .groupby(['Product', 'Size_Value', 'Scent']).size()
                .reset_index(name='Sales with wrong size'))

#outputs
correct_sizes.to_csv(r'.\2022\Week - 19\Output\correct_sizes.csv')
incorrect.to_csv(r'.\2022\Week - 19\Output\incorrect_sizes_agg.csv')

