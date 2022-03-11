
#Import Libraries

from pandas import ExcelFile, read_excel
from numpy import where
from re import sub 

#Load Data
with ExcelFile(r'.\2022\Week - 10\Input\PD Bechdel Test.xlsx') as xl :
    html = read_excel(xl, sheet_name = 'html', header=[0,1])
    df_web = read_excel(xl, sheet_name='Webscraping')

# PROCESS DATA
#clean the column header names
columns = ['Char', 'Numeric code', 'Named code', 'Description']
html.columns = columns
#Replace NaN with empty string
html.fillna(" ", inplace = True)

# Parse out the data in the Download Data field to obtain 'Movie title', 'Pass/Fail
# and movie categorisation
df_web['Categorisation'] = df_web['DownloadData'].str.extract(r'title="\[(.+)\]')
df_web['Pass/Fail'] = where(df_web['DownloadData'].str.extract(r'(\w+).png') == 'nopass',
                            'Fail', 'Pass')
df_web['Title'] = df_web['DownloadData'].str.extract(r'\/view\/\d+\/.+\/">(.*?)<\/a>')

#Create dictionaries to map numeric and named codes to Char
no_code_dict = dict(zip(html['Numeric code'], html['Char']))
name_code_dict = dict(zip(html['Named code'], html['Char']))

patterns = ['(?P<html_code>&#\d+;)', '(?P<html_code>&.*?;)']#numeric, named codes pattern
dicts = [no_code_dict, name_code_dict]

#Replace the html codes with their correct characters
for p, d in zip(patterns, dicts):
    def replace_html(m):
        return d.get(m.group('html_code'))
    df_web['Title'] =df_web['Title'].apply(lambda x: sub(p, replace_html,  x))

# Rank the Bechdel Test Categorisations from 1 to 5, 1 being the best result, 
# 5 being the worst result
category = df_web['Categorisation'].unique().tolist()
rankings = dict(zip(category,[5,4,1,3,2]))
df_web['Ranking'] = df_web['Categorisation'].map(rankings)

# Where a film has multiple categorisations, keep only the worst ranking
df_web.iloc[df_web.groupby(['Title', 'Year'])['Ranking'].idxmin()]

# OUTPUT
df_web.to_csv(r'.\2022\Week - 10\Output\week-10-output.csv', index =False)
print('End')

