
from pandas import ExcelFile, read_excel, date_range
from datetime import timedelta

#Read Data
with ExcelFile(r'.\Data\Absenteeism Scaffold.xlsx') as xl:
    reasons = read_excel(xl, 'Reasons', parse_dates= ['Start Date'])
    

#Process Data
#........................................................................................

#Create End Date field
reasons["End Date"] = [s + timedelta(days = d - 1) for s, d in
                         zip(reasons['Start Date'], reasons['Days Off'])]
# Create an absent Data Range for each an employee 
reasons['Date'] = reasons.apply(lambda row: date_range(
                                    row['Start Date'], row['End Date'], freq= 'd'), axis= 1) 

# Explode dataframe by Absent Date Range
reasons = (reasons.explode('Date', ignore_index= True)).drop(
                            ['Start Date','End Date', 'Days Off'], axis = 1) #Drop columns

# Count number of people off per day
reasons = reasons.groupby('Date')['Name'].count().rename(
                            'Number of People off each day').reset_index()

# Add all dates between 1/04/2021 - 31/05/2021
idx = date_range(reasons.Date.min(), '2021-05-31')
reasons.set_index('Date', inplace=True)
reasons = reasons.reindex(idx, fill_value=0).reset_index().rename(columns={'index': 'Date'})


#OUTPUT
reasons.to_csv(r'.\Output\abscenteeism.csv', index = False)
                                                   