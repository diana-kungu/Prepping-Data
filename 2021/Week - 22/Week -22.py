# Import Libraries
from pandas import ExcelFile, read_excel


#Read Data
with ExcelFile(r'.\Data\Answer Smash Input.xlsx') as xl:
    ans_smash = read_excel(xl, 'Answer Smash')
    names = read_excel(xl, 'Names')
    qns = read_excel(xl, 'Questions')
    cat = read_excel(xl, 'Category')

#PROCESS DATA

# Split Category: Answer in category table
cat[['Category', 'Answer']] = cat['Category: Answer'].str.split(
    ':', expand = True)#.drop('Category: Answer', axis=1)
cat.drop('Category: Answer', axis=1, inplace= True)

#Add Answers to smash table from Category table
ans_smash['Answer'] = [[a for a in cat['Answer'] if s.lower().endswith(a.strip().lower()) ]
        for s in ans_smash['Answer Smash']]    
ans_smash = ans_smash.explode('Answer')

#Add Q No in Names dataframe
names['Q No'] = [ans_smash['Q No'][i] for j in range(len(names)) for i in range(ans_smash.shape[0]) if
                        names['Name'][j] in  ans_smash['Answer Smash'][i] ]

#merge dataframes                         
df_merged = qns.merge(ans_smash).merge(names)

#Output columns
output_cols = [0, 2, 5, 4, 3]
df_merged = df_merged[[df_merged.columns[i] for i in output_cols]]


#OUTPUT
df_merged.to_csv(r'.\Output\smash_answer.csv', index = False)

