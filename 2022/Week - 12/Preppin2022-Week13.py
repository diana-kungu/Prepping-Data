# Prepping data Week 13
# Load Libraries

from pandas import read_csv


#Read Data
df = read_csv(r'.\2022\Week - 13\Input Data\Pareto Input.csv')

# Process Data
#Aggregate the data to the total sales for each customer
df = df.groupby(['Customer ID', 'First Name', 'Surname']).Sales.sum().reset_index()

#Calculate the percent of total sales each customer represents
df['% of Total'] = df['Sales']*100/df['Sales'].sum()

#Order by the percent of total in a descending order
df = df.sort_values(by=['% of Total'], ascending= False)

#Calculate the running total of sales across customers
df['Running % of Total'] = df['% of Total'].cumsum().round(2)

# Create column with total no. unique customers
df['Total Customers'] = len(df)

#Create a parameter that will allow the user to decide the percentage 
# of sales they wish to filter to
select_percent = int(input('Enter a percent Value'))

# Filter data based on selected % 
df_select_percent = df[df['Running % of Total'] <= select_percent]
print(f'{round(len(df_select_percent)*100/len(df))}% of Customers account \
      for {select_percent}% of Sales ')

df_select_percent

#Output
df_select_percent.to_csv(r'.\2022\Week - 13\Output\pareto_analysis.csv', index = False)
print('End')
