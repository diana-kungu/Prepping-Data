#Imports
from pandas import ExcelFile, read_excel, merge

#Read data
with ExcelFile(r'.\2021\Week - 38\Inputs\Trilogies Input.xlsx') as xl :
    films = read_excel(xl, sheet_name = 'Films' )
    df_t = read_excel(xl, sheet_name = 'Top 30 Trilogies' )


#Process Data
# Clean films names
films[['Film Order', 'Total Films in Series']] = films['Number in Series'].str.split(
                                                 '/', expand= True
                                                    )
films.drop('Number in Series', axis=1, inplace=True)

#Find Trilogy Average rating
films['Trilogy Average'] = films.groupby('Trilogy Grouping')['Rating'].transform('mean')#.round(1)

#Find Max Rating per trilogy and rank by trilogy avg and max rating per trilogy
films['Max Trilogy Rating'] = films.groupby('Trilogy Grouping')['Rating'].transform('max')#.round(1)
films["Trilogy Ranking"] = films[['Trilogy Average', 'Max Trilogy Rating']].apply(tuple,axis=1)\
             .rank(method='dense',ascending=False).astype(int)

films.sort_values(['Trilogy Average', 'Max Trilogy Rating'], ascending=False, inplace=True)

#Clean trilogy names and merge with films dataset
df_t['Trilogy'] =df_t['Trilogy'].str.replace(' trilogy', '')
films.drop(['Trilogy Grouping', 'Max Trilogy Rating'], axis=1, inplace=True)
df_combined = merge(df_t, films, how='inner')
df_combined['Trilogy Average'] = df_combined['Trilogy Average'].round(1)


#Output
df_combined.to_csv(r'.\2021\Week - 38\Output\week_38_output.csv', index=False)
print('End')