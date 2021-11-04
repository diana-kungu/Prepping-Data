#IMPORTS
from pandas import ExcelFile, read_excel
from os import chdir
from re import split

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#READ DATA
with ExcelFile(r'.\Data\Week19_Input.xlsx') as xl:
    updates = read_excel(xl, 'Project Schedule Updates')
    projects = read_excel(xl, 'Project Lookup Table')
    sub_projects = read_excel(xl, 'Sub-Project Lookup Table')
    tasks =read_excel(xl, 'Task Lookup Table')
    owner = read_excel(xl, 'Owner Lookup Table')

#PROCESS DATA

#Create new index Week + week number
updates.index = 'Week ' + updates['Week'].astype(str)

# Each commentary on independt rows
updates = updates['Commentary'].str.split('\s+(?=\[)').explode().str.strip().reset_index()

#Parse different fields from commentary column
updates[['Project Code', 'Sub-Project Code', 'Task Code', 'Details']]  = updates['Commentary']\
                                    .str.extract('\[(\w+)\/(\w+)-(\w+)\]\s(.+)')

updates['Abbreviation'] =   updates['Commentary']\
                                    .str.extract('\.\s+(\w+)\.')    

updates['Days Noted'] =   updates['Commentary']\
                                    .str.extract('.*?(\d)\sdays')  

#Drop Commentary field and fillnans
updates.drop('Commentary', axis= 1, inplace= True)
updates.fillna("", inplace= True)      

# Update Names
owner_dict = dict(zip(owner['Abbreviation'], owner['Name']))
updates['Name'] = updates['Abbreviation'].str.title().map(owner_dict)

# Update Project, Tasks and Sub Projects
projects_dict = dict(zip(projects['Project Code'], projects['Project']))
task_dict = dict(zip(tasks['Task Code'], tasks['Task']))
sub_dict = dict(zip(sub_projects['Sub-Project Code'], sub_projects['Sub-Project']))

updates['Project'] = updates['Project Code'].map(projects_dict )
updates['Sub-Project'] = updates['Sub-Project Code'].str.lower().map(sub_dict)
updates['Tasks'] = updates['Task Code'].map(task_dict)

cols = ['Week', 'Project', 'Sub-Project', 'Tasks', 'Name', 'Days Noted', 'Details']
updates =  updates[cols]


#OUTPUT
updates.to_csv(r'.\Output\week-19.csv', index = False)