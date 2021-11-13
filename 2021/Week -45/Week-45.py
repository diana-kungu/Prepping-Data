# IMPORTS
from pandas import ExcelFile, read_excel, concat, merge
from datetime import datetime


chdir(r"c:\Users\DIANA\Desktop\Prepping_data")


# PROCESS DATA
#...................................................................................
#Read Data
xl=  ExcelFile(r'.\Data\TC Input.xlsx') 
sheets = xl.sheet_names
df = concat([read_excel(xl,  sheet_name=s) #
                .assign(Date=s) for s in sheets[:-1]], axis= 0, ignore_index= True)

attendees = read_excel(xl, sheet_name=sheets[-1])

#Convert Attendee IDs to list
df['Attendee IDs'] = df['Attendee IDs'].apply(lambda x : x.split(','))

#Make a Datetime field
df['Date'] = df['Date'].str.replace('th ', '-')+'-2021'
df['Session Time'] = [str(x)+':00:00' if len(str(x)) <= 2 else x for x in df['Session Time']]
df['Date'] = df['Date'] + " " + df['Session Time'].astype('str')

#Convert Date string to datetime object
df['Date'] = list(map(lambda x :datetime.strptime(x, '%d-%b-%Y %H:%M:%S'), df['Date']))

#Eplode dataframe:- Each Attendee on independent row
df_expld = df.explode('Attendee IDs').reset_index(drop = True)

#Harmonize data type for merging columns
attendees['Attendee ID'] = attendees['Attendee ID'].astype(str).str.strip()
df_expld['Attendee IDs'] = df_expld['Attendee IDs'].str.strip()

#Merge with Attendees Dataframe to match code and names of attendee
df_combined = merge( df_expld, attendees, how= 'left', left_on='Attendee IDs', right_on= 'Attendee ID')


#A function that takes attendee codes and return their direct contacts in each session
def get_direct(row):
    code = row['Attendee ID']
    topic = row['Subject']
    date = row['Date']

    direct = []
    for i in range(len(df)):
        ids = [x.strip() for x in df['Attendee IDs'].iloc[i]]
        if df['Date'].iloc[i] == date and code in ids and\
            df['Subject'].iloc[i] == topic:

            direct.extend(ids)
    return (set(direct)).difference([code])

#Generate the direct contacts column
df_combined['Direct-contacts-codes'] = df_combined.apply(get_direct, axis=1)

# Explode to create a row for each attendee and direct contact
df_combined = df_combined.explode('Direct-contacts-codes')

# Drop duplicates
df_combined = df_combined.drop_duplicates(subset=['Subject', 'Attendee ID', 'D-codes'], keep='last')\
                   .reset_index(drop= True)

# Merge with Attendees df to match direct contacts code and names
df_direct = merge( df_combined, attendees, how= 'left', left_on='Direct-contacts-codes', right_on= 'Attendee ID')

#..........................................................................................................
# INDIRECT CONTACTS
#..........................................................................................................
# Function that capture indirect attendees
def get_indirect(row):
    drct_code = row['D-codes']
    attendee_code = row['Attendee ID']
    topic = row['Subject']
    date = row['Date']

    #Get list of all  direct contacts (codes) of  a given attendee and subject
    mini_df = df_direct[(df_direct['Attendee IDs'] == attendee_code) & (df_direct['Subject'] == topic)]
    direct_codes = list(mini_df['D-codes'].values)
    #direct_codes = [attendees[attendees['Attendee'] == i].iloc[0,0] for i in direct_names]
    
    indirect = []
    for i in range(len(df)):
        ids = [x.strip() for x in df['Attendee IDs'].iloc[i]]
        if df['Date'].iloc[i] <= date and drct_code in ids and\
            df['Subject'].iloc[i] == topic:

            indirect.extend(ids)
    return (set(indirect)).difference(direct_codes)#

# Generate indirect Contacts for each row
df_combined['Indirect_contacts'] = df_combined.apply(get_indirect, axis= 1)

# Explode to flatten Indirect contacts column
df_combined = df_combined.explode('Indirect_contacts')

# Drop duplicates
df_combined = df_combined.drop_duplicates(subset=['Attendee ID', 'Indirect_contacts', 'Subject'])

# Merge:- 
df_indirect = merge( df_combined, attendees, how= 'left', left_on='Indirect_contacts', right_on= 'Attendee ID')

# Remove rows that have attendee being their own indirect contact
dups = df_indirect[df_indirect['Attendee_x'] == df_indirect['Attendee_y']].index
df_indirect.drop(dups, axis=0, inplace= True)

# OUTPUT
#.......................................................................................................
#Create contact type column for both direct and indirect dataframe
df_indirect['Contact Type'] = 'Indirect'
df_direct['Contact Type'] = 'Direct Contact'

#Select the output columns are rename
output_cols = ['Subject', 'Attendee_x', 'Contact Type', 'Attendee_y']
col_names= ['Subject', 'Attendee', 'Contact Type', 'Contact']

df_indirect = df_indirect[output_cols]
df_indirect.columns = col_names

df_direct = df_direct[output_cols]
df_direct.columns = col_names

#Join the indirect and direct dataframe
tc_df = concat([df_indirect, df_direct], ignore_index= True)

#SAVE OUTPUT
tc_df.to_csv(r'.\Output\week45-tc.csv', index=False)

