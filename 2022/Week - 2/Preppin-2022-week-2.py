# Preppin Data week 2- 2022

# Import Libraries
from pandas import read_csv
from numpy import where
from datetime import datetime, timedelta
from pandas.testing import assert_frame_equal # testing output


#Read Data
df = read_csv(r'.\2022\Week - 1\Input\preppin_input_week_1.csv', parse_dates=['Date of Birth'],
              usecols=['pupil first name', 'pupil last name', 'Date of Birth'])


# ...............................................................................................
# Process Data
# Creaate pupils names and This years's Birthday field
df["Pupil Name"] = df['pupil first name'] +' ' +  df['pupil last name']  
df = df[["Pupil Name", "Date of Birth"]].copy()
df["This Year's Birthday"] = df['Date of Birth'].map(lambda x: x.replace(year= datetime.now().year))
# Birthday Month and day of week (where BD falls on weekend shift to Friday)
df['BD Adjusted'] = [x + timedelta(days=-1) if x.date().strftime("%A") == "Saturday"
                     else x + timedelta(days=-2) if x.date().strftime("%A") == "Sunday"
                     else x for x in df['This Year\'s Birthday']]
df["Cake Needed On"] = df["BD Adjusted"].dt.day_name()
df["Month"] = df["BD Adjusted"].dt.month_name()
#Group by month and day of week and count number of pupils
df['BDs per Weekday and Month'] = df.groupby(['Month', 'Cake Needed On' ])["Pupil Name"].transform('count')

# Compare output with given results
results = read_csv(r".\2022\Week - 2\Input\res.csv", 
                   parse_dates=['Date of Birth', "This Year's Birthday"], dayfirst= True)
assert_frame_equal(results, df)
#..............................................................................................................


#OUTPUT
df.to_csv(r'.\2022\Week - 2\Output\birthday_schedule.csv', index=False)


