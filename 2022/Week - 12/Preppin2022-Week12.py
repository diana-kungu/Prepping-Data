# Prepping data week 12
# Load Libraries
from pandas import read_csv, concat, merge
import zipfile


# Read Data
cols = ['EmployerSize', 'EmployerName', 'EmployerId', 'DiffMedianHourlyPercent']
with zipfile.ZipFile(r'.\2022\Week - 12\Input\Inputs-20220325T054254Z-001.zip') as zip_fl:
    files = zip_fl.namelist()
    df = concat(read_csv(zip_fl.open(i), usecols =cols).assign(Year= i) for i in files)


# PROCESS DATA

#Extract the Report years from the file paths
df['Report'] = df['Year'].str.extract(r'(\d+\s.+\d+)')
#Create a Year field based on the the first year in the Report name
df['Year'] = df['Year'].str.extract(r'([0-9]+)').astype('int')

#Some companies have changed names over the years. For each EmployerId, 
# find the most recent report they submitted and apply this EmployerName 
# across all reports they've submitted

update_names = (df.groupby(['EmployerId'], as_index= True)
                        .apply(lambda x: x.loc[x['Year'].idxmax(), 'EmployerName'])
                        .reset_index().rename(columns ={0: 'EmployerName'}))

df = df.drop('EmployerName', axis=1).merge(update_names, on='EmployerId')

#Create a Pay Gap field,  a positive DiffMedianHourlyPercent means the women's
# pay is lower than the men's pay, whilst a negative value indicates the other way around
df['Pay Gap'] = (df['DiffMedianHourlyPercent'].apply(lambda x: 
                      f"In this organisation, women's median hourly pay is {x} % lower than men's" if x > 0 else
                      
                      ("In this organisation, women's median hourly pay is {x}% higher than men's" if x > 0
                      else
                      "In this organisation, men's and women's median hourly pay is equal."
                      )))
df.to_csv(r'.\2022\Week - 12\Output\Gender_pay_gap.csv', index= False)
print('End')

