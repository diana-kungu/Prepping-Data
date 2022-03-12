
#Import Libraries
from pandas import read_csv, qcut, melt, merge, cut, Series
from os import getcwd, chdir
from numpy import mean
#chdir(r'c:\Users\DIANA\Desktop\Projects\Prepping_data\2022')
print(getcwd())


#Read Data
df = read_csv(r'.\Week - 3\Input\Grades.csv')
df_grades = df.copy()

# Divide the students grades into 6 evenly distributed groups 
grades = ['F', 'E', 'D', 'C', 'B', 'A']
for col in df_grades.columns[1:]:
    df_grades[col]= qcut(df_grades[col], q=6, labels= grades)

#Convert the groups to two different metrics: 
#The top scoring group should get an A, second group B etc through to the sixth group who receive an F
# An A is worth 10 points for their high school application, B gets 8, C gets 6, D gets 4, E gets 2 and F gets 1
df_melted = df.melt(id_vars=['Student ID'], var_name='Subject', value_name='Score')
df_melted = df.melt(id_vars=['Student ID'], var_name='Subject', value_name='Score')
df_grades = df_grades.melt(id_vars=['Student ID'], var_name='Subject', value_name='Grade')
df = merge(df_melted, df_grades)
 
score = [1, 2, 4, 6, 8, 10]
score_dict =dict(zip(grades, score))
df['Points'] =df['Grade'].replace(score_dict)

#Determine how many high school application points each Student has received across all their subjects 
#Work out the average total points per student by grade
df['Total Points per Student'] = df.groupby('Student ID').Points.transform('sum')
df['Avg student total points per grade'] = (df.groupby(['Grade'])
                                                   ['Total Points per Student'].transform('mean')).round(2)

# Take the average total score you get for students who have received at least one A 
# and remove anyone who scored less than this
avg_with_a =df[df['Grade'] == 'A']['Avg student total points per grade'].min()
df = df[(df['Total Points per Student'] >avg_with_a) & (df['Grade'] !='A')].copy()

# How many students scored more than the average if you ignore their As?
df['Total Points without As']= df.groupby('Student ID')['Points'].transform('sum')

print(f"{df} scored more than average without As")


print('End')