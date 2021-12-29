#Import Libraries
from pandas import ExcelFile, read_excel, merge


#Read Data
with ExcelFile(r'.\2021\Week - 52\\Input\PD 2021 Wk 52 Input.xlsx') as  xl:
    df_complaints = read_excel(xl, sheet_name = 'Complaints' )  
    keywords = read_excel(xl, sheet_name = 'Department Responsbile' )

# Process Data
#Count the number of complaints per customer
df_complaints['complaints per customer'] = df_complaints.groupby(['Name'],
                                                                 as_index = False)['Complaint'].transform('count')
# Create 'other' keyword
keywords = keywords.append( {'Keyword':'other', 'Department': 'Unknown'}, ignore_index= True)
keywords_dict = dict(zip(keywords['Keyword'], keywords['Department']))

df_complaints['Complaints causes'] = [[i for i,v in keywords_dict.items() if i.lower() in k] 
                                        for k in df_complaints['Complaint']]

#Allocate the complaints to the correct department
df_complaints = df_complaints.explode('Complaints causes') 
df_complaints.fillna('other', inplace= True) 
df_complaints = df_complaints.merge(keywords, how='left', left_on= 'Complaints causes', 
                                    right_on = 'Keyword')

#Create a comma-separated field for all the keywords found in the complaint for each department
df_complaints['Complaints causes'] = df_complaints.groupby(['Name', 'Complaint', 'complaints per customer', 
                                            'Department'])['Complaints causes'].transform(lambda x: ', '.join(x))
df_complaints.drop('Keyword', axis=1, inplace= True)
df_complaints.drop_duplicates(inplace= True)

#OUTPUT
df_complaints.to_csv(r'.\2021\Week - 52\Output\week-52-output.csv', index= False)


