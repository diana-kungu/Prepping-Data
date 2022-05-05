# Prepping Data week 17
#Load libraries
from pandas import ExcelFile, read_excel, to_datetime, merge, concat
from numpy import where

#Read data
with ExcelFile(r'.\2022\Week - 17\Input\2022W17 Input.xlsx') as  xl:
    df = read_excel(xl, sheet_name = 'Streaming', converters={'t': to_datetime})
    pricing = read_excel(xl, sheet_name = 'Avg Pricing' )

# PROCESS
#Fix the date so they are recognised as date data types
df['t'] = df['t'].dt.tz_localize(None)

# Correct the spelling in location field
df['location'] = df['location'].str.replace('Edinurgh', 'Edinburgh')
#Aggregate the data to find the total duration of each streaming session 
df['duration'] = (df.groupby(['userID', 't', 'location'],
                    as_index= False ).duration.transform(sum)
                 )
df.drop_duplicates(inplace= True)

#update the content_type field:
##    For London, Cardiff and Edinburgh, the content_type is defined as "Primary"
##    For other locations, maintain the "Preserved" content_type and 
# update all others to have a "Secondary" content_type
df['content_type'] = where(df['location'].isin(['London', 'Cardiff', 'Edinburgh']),"Primary",
                        where(((df['content_type'] =='Preserved') &
                              (~df['location'].isin(['London', 'Cardiff', 'Edinburgh']))),
                              "Preserved", "Secondary")                           
                           )
# Rename columns
df.rename(columns={'content_type': 'Content_Type', 't': 'Timestamp'}, inplace= True)
# Create Month and Year fields 
pricing[['Month_ded', 'Year']] = pricing['Month'].str.split(' ', expand=True).astype('int')
df['Year'], df['Month_ded'] = zip(*df['Timestamp'].apply(lambda x: (x.year, x.month)))

# Merge pricing df and streaming df
df_merged = df.merge(pricing, how='left', on=['Year', 'Month_ded', 'Content_Type'])

#Update Avg_Price field For "Primary" content,
# we take the overall minimum streaming month, ignoring location For all other content,
# we work out the minimum active month for each user, in each location and for each content_type
prim_avg = (df_merged[(df_merged['Content_Type'] == 'Primary')]
                .sort_values(by= ['Year','Month_ded', 'Timestamp'])
                    .groupby(['userID']).Avg_Price.transform('first')
            )
sec_avg_price = (df_merged[df_merged['Content_Type'] == 'Secondary']
                                .sort_values(by= ['Year','Month_ded', 'Timestamp'])
                                .groupby(['location', 'userID']).Avg_Price.transform('first')
                )
#Concat primary and secondary  avg_price series
avg_prices = concat([prim_avg, sec_avg_price]).to_frame()
# Update Avg_Price field
df_merged = df_merged.drop('Avg_Price', axis= 1).merge(avg_prices, how= 'left', 
                                           left_index=True, right_index=True)
# For "Preserved" content, manually input the Avg Price as £14.98
df_merged['Avg_Price'] = where(df_merged['Content_Type'] == 'Preserved', 14.98,
                               df_merged['Avg_Price'])

#Output
df_merged.to_csv(r'.\2022\Week - 17\Output\streaming_rcd.csv', index = False)
print('End')

