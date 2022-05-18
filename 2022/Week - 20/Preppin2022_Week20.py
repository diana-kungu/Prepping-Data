
#Load Modules
from pandas import ExcelFile, read_excel, merge, concat
from numpy import size


# Read Data
with ExcelFile(r'.\2022\Week - 20\Inputs\TC22 Input.xlsx') as  xl:
    reg = read_excel(xl, sheet_name = 'Registrations' )
    sessions = read_excel(xl, sheet_name = 'Sessions' )
    online = read_excel(xl, sheet_name = 'Online Attendees' )
    in_person = read_excel(xl, sheet_name = 'In Person Attendees' )

#Process Data
#In the Registrations Input, tidy up the Online/In Person field
replacements = {
            'Online/In Person': {
                r'(On.*)': 'Online',
                r'(I\w\sP.+)': 'In Person'
            }
}
reg.replace(replacements, regex=True, inplace=True)

#From the Email field, extract the company name 
reg['Company Name'] = reg['Email'].str.extract('\S+@(\S+)\.\w+$')
#Count the number of sessions each registered person is planning to attend
reg['No. of Sessions'] = reg.groupby('Email')['First Name'].transform(size)

#Join on the Session Lookup table to replace the Session ID with the Session name
reg = reg.merge(sessions)

#Join the In Person Attendees dataset to the cleaned Registrations
# return the names of those that did not attend the sessions they registered for
#absent from in person sessions
in_person_absent = (in_person.merge(reg[reg['Online/In Person'] == 'In Person'], how= 'outer', 
                     on=['Session', 'First Name', 'Last Name'], indicator= True)
     .query('_merge=="right_only"'))

#Absent from online sessions
online_absent = (online.merge(reg[reg['Online/In Person'] == 'Online'], how= 'outer', 
                     on=['Session', 'Email'], indicator= True)
     .query('_merge=="right_only"'))

# Join the absentees from online and in Person sessions
absentees = concat([online_absent, in_person_absent], ignore_index= True)

# Count the number of sessions each person was unable to attend
# Calculate the % of sessions each person was unable to attend 
absentees['Sessions not Attended'] = (absentees.groupby('Email')['First Name']
                                      .transform(size))
absentees['% Not Attended'] = (absentees['Sessions not Attended']*100/
                               absentees['No. of Sessions']).round(2)

# Output
absentees_cols = ['Company Name', 'First Name', 'Last Name', 'Email', 
                  'Online/In Person', 'Session', '% Not Attended']
absentees.to_csv(r'.\2022\Week - 20\Output\TC22_absentees.csv', 
                 columns= absentees_cols, index= False)
print('End')

