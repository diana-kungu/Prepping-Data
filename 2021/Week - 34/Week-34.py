
#Imports
from pandas import ExcelFile, read_excel, melt, merge
from numpy import where
from pandas.core import indexing


#Read Data
with ExcelFile(r'.\2021\Week - 34\2021 Week 34 Input.xlsx') as xl :
    sales = read_excel(xl, sheet_name = 'Employee Sales' )
    targets = read_excel(xl, sheet_name = 'Employee Targets' )

# PROCESS DATA
#Melt dataframe
sales = sales.melt(id_vars = ['Store', 'Employee'], var_name='Month', value_name='Sales')
sales.Month = sales.Month.dt.month_name()

#Calculate the Average Monthly Sales for each employee
sales['Avg. Monthly Sales'] = sales.groupby(['Store','Employee'])['Sales'].transform('mean').round(0).astype('int')

#Cleanup targets sheet the Store Name
targets['Store'] = targets.Store.replace(['^S.+d$', '^[WV].+', '^Br.+', '^Y.+'],
                                ['Stratford', 'Wimbledon', 'Bristol', 'York'], regex = True)

# Merge with target records
df_combined = merge(sales, targets, how='left', left_on=['Store', 'Employee'], right_on=['Store', 'Employee'])

#Filter the data so that only employees who are below 90% of their target on average remain
df_combined['% on Target'] = (df_combined['Avg. Monthly Sales']*100/df_combined['Monthly Target']).astype('int')
df_combined = df_combined[df_combined['% on Target']<90]
df_combined['Above Target?']= where(df_combined['Sales']> df_combined['Monthly Target'], 1,0)

#For these employees, we also want to know the % of months that they met/exceeded their target
df_results = df_combined.groupby(['Store', 'Employee']).agg(Avg_monthly_Sales=('Sales', 'mean'),
                                                   pct_of_months_target_met=('Above Target?', 'mean'),
                                                   Monthly_Target=('Monthly Target', 'mean'))\
                                              .reset_index()

# Format the data 
df_results.iloc[:,[2,4]] = df_results.iloc[:,[2,4]].applymap(lambda x: int(x))
df_results['pct_of_months_target_met'] =(df_results['pct_of_months_target_met']*100).round(0).astype('int')

#OUTPUT
df_results.to_csv(r'.\2021\Week - 34\Week34_output.csv', index =False)


