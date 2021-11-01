#Import libraries
from pandas import read_csv, date_range, to_datetime, DatetimeIndex
from os import getcwd, chdir

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#READ DATA
data = read_csv(r'.\Data\Week42.csv', parse_dates= [0], index_col= 0, dayfirst= True)

#PROCESS DATA
#Create rows for the missing Dates
idx = (date_range(to_datetime(data.index[0]), to_datetime(data.index[-1])))
data = data.reindex(idx, method = 'ffill')

#Create required fields: Days into fund, Avg raised per weekday and Date(weekday)
data["Days into fund raising"] = [r for r in range(len(data))]
data["Date"] = data.index.day_name()
data['Value raised per day'] = data['Total Raised to date']/data['Days into fund raising']
data['Avg raised per weekday'] = data.groupby('Date')['Value raised per day'].transform('mean')

#Clean/format dataframe
data.sort_values('Date',ascending= False, inplace= True)
data.reset_index(drop = True, inplace= True)
data['Total Raised to date'] = data['Total Raised to date'].astype(int)
data.fillna('', inplace= True)

# Rearrange columns in the final output dataframe
cols = [4, 3, 1, 2, 0] 
data = data[[data.columns[i] for i in cols]]


#OUTPUT
data.to_csv(r'.\Output\week42_output.csv', index = False)
