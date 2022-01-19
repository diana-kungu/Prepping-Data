
# Preppin Data week 3- 2022

# Import Libraries
from pandas import read_csv, merge, melt


#Read Data
students = read_csv(r'.\2022\Week - 1\Input\preppin_input_week_1.csv',
                   usecols=['id','pupil first name', 'pupil last name', 'gender'])
grades = read_csv(r'.\2022\Week - 3\Input\Grades.csv')

## Process Data
#Rename column
students.rename(columns={'id': 'Student ID'}, inplace= True)
# Merge grades and students datasets
df = students.merge(grades)
# Convert to long format
df = melt(df, id_vars=['Student ID', 'pupil first name', 'pupil last name', 'gender'],
     value_name='Score', var_name= 'Subject')
#Passed Flag: Pass score 75 and above
df['Passed Flag'] = [1 if x > 74 else 0 for x in df['Score']]

#Aggregate per Student: Average score and number of passed subjects
df = df.groupby(['Student ID','gender'], as_index= False).agg(
                Avg_Score = ('Score', 'mean'),
                Passed_Subjects = ('Passed Flag', 'sum'))

df['Avg_Score'] =df['Avg_Score'].round(1)

# Output
df.to_csv(r'.\2022\Week - 3\Ouput\prepped-week-3-output.csv', index= False)
print("End")


