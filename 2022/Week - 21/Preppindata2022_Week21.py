# load libraries
from pandas import read_excel, ExcelFile, concat, melt, pivot_table, merge

# Read Data
workbook =  ExcelFile(r'.\2022\Week - 21\Input\2022W21 Input.xlsx')
sheets = workbook.sheet_names
df = (concat([read_excel(workbook, sheet_name = s, skiprows=3, nrows=11,
                   usecols=lambda x: x if not str(x).startswith('FY') and x != 'Comments' else None )
              .assign(Store= s) for s in sheets ], ignore_index= True )
              .ffill()
)

#Reshape the data so that we have a Date field
df = melt(df, id_vars=['Department' ,'Target', 'Breakdown', 'Store'], var_name= 'Date')
#For Orders and Returns, we are only interested in reporting % values, 
# whilst for Complaints we are only interested in the # Received
mask = (
        (df['Department'].isin(['Orders', 'Returns'])) & (df['Breakdown'].str.startswith('%'))
        | ((df['Department'] == 'Complaints') & (df['Breakdown'] == '# Received'))
        )
df = df[mask]

# Parse breakdown metrices
df['actual'] = [x.split(' ')[0] + ' ' + y + ' ' + ' '.join(x.split(' ')[1:]) 
                for x , y in zip(df.Breakdown, df.Department)]
df['target_metrices']= 'Target - ' + df['actual']
df['Target_values'] = (df['Target'].str.replace('[>|%]', '', regex = True)
                       .fillna(0)).astype(int)/100

# Pivot target and actual measures
df = merge(pivot_table(df,index=['Store', 'Date'], columns='actual', values= 'value').reset_index(),
     pivot_table(df,index=['Store', 'Date'], columns='target_metrices', values= 'Target_values').reset_index())
        
#Output
df.to_csv(r'.\2022\Week - 21\Output\week21_output.csv', index = False)
print('prepped!')

