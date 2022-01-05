
# Import Libraries
from pandas import read_csv, date_range, DataFrame, PeriodIndex
from numpy import where
from pandas.testing import assert_frame_equal # testing output
from os import getcwd


#Read Data
df = read_csv(r'.\2022\Week - 1\Input\preppin_input_week_1.csv', parse_dates=['Date of Birth'])

# ...............................................................................................
# Process Data
# Creaate pupils/parent names and email addresses
df["Pupil's Name"] = df['pupil last name']  +', ' + df['pupil first name']

df["Parental Contact Full Name"] = where(df['Parental Contact'] == 1,
                                         df['pupil last name'] +', ' + df['Parental Contact Name_1'],
                                         df['pupil last name'] +', ' + df['Parental Contact Name_2']
                                        )

df["Parental Contact Email Address"] =  where(df['Parental Contact'] == 1,
                                              df['Parental Contact Name_1'] + "."+ df['pupil last name']+"@" + df["Preferred Contact Employer"] + ".com",
                                              df['Parental Contact Name_2'] + "."+ df['pupil last name']+"@" + df["Preferred Contact Employer"] + ".com"
                                            )                                           
# Academic Year
df = df.assign(Academic_Year= PeriodIndex(df['Date of Birth'], freq='A-Aug'))
df["Academic_Year"] = df["Academic_Year"].map(lambda x: int(x.strftime('%Y'))) 
df["Academic_Year"] = where(df["Academic_Year"] >=2015, 1,
                            (2015 - df["Academic_Year"] )+1)
#..............................................................................................

#Output
df.rename(columns={"Academic_Year": "Academic Year"},inplace= True)
output_cols = ["Academic Year", "Pupil's Name", "Parental Contact Full Name", "Parental Contact Email Address" ]
df_output = df[output_cols]
df_output.to_csv(r'.\2022\Week - 1\Output\preppin-2022-output-week-1.csv', index= False)

# Compare output with given results
results = read_csv(r".\2022\Week - 1\Input\week_1_ouput.csv")
assert_frame_equal(results, df_output)

print('Complete')

