
#load modules
from pandas import read_csv, merge, melt, DataFrame, concat
from numpy import where

#Read data
df = read_csv(r'.\2022\Week - 23\Input\Opportunity.csv', 
              parse_dates=['CreatedDate', 'CloseDate'], dayfirst=True)
history = read_csv(r'.\2022\Week - 23\Input\Opportunity History.csv', 
                   parse_dates=['CreatedDate'], dayfirst=True)


#Processing
#--------------------------------------------------------------------------------------------------
#Pivot the CreatedDate & CloseDate fields so that we have a row for when each opportunity Opened and
# a row for the ExpectedCloseDate of each opportunity

df_mlt = (melt(df, id_vars=['Id', 'StageName', 'Name'], 
              value_vars=['CreatedDate', 'CloseDate'], value_name='Date' )
        .rename(columns={'Name': 'Stage'} #Rename the Names field to Stage 
        ))
#Update the Stage field so that if the opportunity has closed
# the ExpectedCloseDate is updated with the StageName
df_mlt.StageName = where(((df_mlt.variable == 'CloseDate') &
                                (~df_mlt['StageName'].isin(['Closed Won', 'Closed Lost']))), 'ExpectedCloseDate',
                    where(df_mlt.variable == 'CreatedDate', 'Opened', df_mlt.StageName))

#Remove unnecessary fields and rename columns
df_mlt = df_mlt[['Id', 'Date', 'StageName']].rename(columns={'Id': 'OppID',
                                                    'Date': 'CreatedDate'})

#Extract StageName and SortOrder field column fro history table
# Add SortOrder for Opened and ExpectedCloseDate variables
s_order = history[['StageName', 'SortOrder']].drop_duplicates()
s_order = s_order.append(DataFrame({'StageName': ['ExpectedCloseDate', 'Opened'],
                        'SortOrder': [11, 0]}), ignore_index= True
                        )

#Merge sortOrders df to add SortOrders to df_mlt
df_mlt = df_mlt.merge(s_order)

#Bring in the additional information from the Opportunity History
# table about when each opportunity moved between each stage
df_mlt = concat([df_mlt, history], ignore_index= True)

#Remove duplicate rows 
df_mlt = df_mlt.drop_duplicates()

#OUTPUT
df_mlt.to_csv(r'.\2022\Week - 23\Output\week23.csv', index= False)
print('End!')
