#Imports
from pandas import read_csv, pivot_table, pivot
from os import getcwd


#Read Data
df = read_csv(r'.\2021\Week - 31\PD_2021_wk31_input.csv', parse_dates=['Date'], dayfirst=True)

#Remove the 'Return to Manufacturer' records
df = df.drop(df[df['Status']=='Return to Manufacturer'].index, axis=0)

#Create a total for each Store of all the items sold 
df['Items Sold per Store'] = df.groupby(['Store'], as_index = False)['Number of Items'].transform('sum')
#Aggregate the data to Store sales by Item
df_p = (df.pivot_table(index=['Store', 'Items Sold per Store'], 
                columns='Item', values='Number of Items', aggfunc='sum')).reset_index()


# Output
df_p.to_csv(r'Week31_output.csv', index = False)
print("end")

