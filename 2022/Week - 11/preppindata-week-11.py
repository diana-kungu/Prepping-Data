
#Week 11

#Load modules
from pandas import read_csv

#Read Data
df = read_csv(r'.\2022\Week - 11\Input\PD Fill the Blanks challenge.csv')


# Groupby Weekday, Teach and lesson time and fillna with first
df[['Lesson Name', 'Subject']] = df.groupby(['Weekday', 'Teacher', 'Lesson Time'])\
                                    [['Lesson Name', 'Subject']].transform('first')
# Compute average Attendance per Lesson and Subject per weekday
df['Avg. Attendance per Subject & Lesson'] = df.groupby(['Weekday', 'Teacher', 'Lesson Time'])\
                                    ['Attendance'].transform('mean').round(2)


#Output
df.to_csv(r'.\2022\Week - 11\Output\week-11.csv', index = False)
print('end')


