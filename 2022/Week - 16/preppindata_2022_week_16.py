# Week 16
#Load Libraries
from pandas import read_excel, ExcelFile, concat,merge
from numpy import hsplit, split


#Read Data
with ExcelFile(r'.\2022\Week - 16\Input\Menu Input.xlsx') as xl :
    df = read_excel(xl, sheet_name = 'Orders', header=None )
    menu = read_excel(xl, sheet_name = 'Lookup Table' )

# Process Data
# Split by blank column
df_list = hsplit(df, df.columns[df.isnull().all()])

##Reshape the Orders table so that we h ave 3 columns:
# Guest name, Dish, Selections (containing 🗸 or null)
df_reshaped = []
for df_guest in df_list:
    df_guest = df_guest.dropna(how='all', axis=1)
    df_guest = df_guest.assign(Guest=df_guest.iloc[0,0]).drop(0)
    df_guest.columns = ['Dish', 'Selection', 'Guest Name' ]
    df_reshaped.append(df_guest)
df = concat(df_reshaped, ignore_index= True)

#Rename course
df.Dish = df.Dish.replace(['Starter', 'Main', 'Desserts'], ['Starters', 'Mains', 'Dessert'])
#Extract the course name from the Dish field
courses_splt = df[df['Dish'].isin(['Starters', 'Mains', 'Dessert'])].index[1:]
df = concat([i.assign(Course= i.iloc[0]['Dish']) for i in split(df, courses_splt)])

#Filter out where the Dish = Course & dishes which have not been selected
df = df[(df['Dish'] != df['Course']) & (df['Selection'].notna())].copy()
# Merge with lookup table to include recipe information
df = merge(df, menu)

#Output
df =(df.iloc[:, [2,3,4,0]])
df.to_csv(r'.\2022\Week - 16\Output\week_16_output.csv', index = False)
print('End')


