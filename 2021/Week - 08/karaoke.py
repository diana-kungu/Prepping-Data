import pandas as pd
import os

session_lst = []

def session(df):
    s = 1
    for i in range(len(df_songs)):
        if i == 0:
            session_lst.append(1)
                        
        else: 
            if df['time_diff'][i] <= 59:
                session_lst.append(s)
                
            else:
                s += 1
                session_lst.append(s)
                                
    return session_lst

#print(os.getcwd())

#READ DATA
xl = pd.ExcelFile(r'./Data/Karaoke.xlsx')
#Parse and sort the df by dates
df_songs = xl.parse(0)
df_songs.sort_values(by="Date", inplace= True)
df_customers = xl.parse(1)
df_customers.sort_values(by="Entry Time", inplace= True)


#PROCESS DATA
#Set Datetime object to dd-mm-yyyy hh-mm-ss format and create time diff field
df_songs.Date = df_songs.Date.dt.round('1s')
df_songs["time_diff"] = (df_songs["Date"] - df_songs["Date"].shift(1)).astype('timedelta64[m]').fillna(0)

#Match each song to a session ID
session_lst = []
df_songs["Session"] = session(df_songs)
df_songs["Song Order"] = df_songs.groupby('Session')['Date'].rank(method = 'first').astype('int')

#Groupby session and get first
first_per_session = df_songs.groupby('Session').first().reset_index()[["Date", "Session"]]

#Match the customers to the correct session, based on their entry time
customer_first_session = pd.merge_asof(df_customers, first_per_session,
                                        left_on = "Entry Time", right_on = "Date", 
                                        tolerance = pd.Timedelta(minutes=10), direction='forward').dropna()
final = pd.merge(df_songs, customer_first_session, how= 'left', on= "Session", suffixes = ["", "_y"] )
final.drop('Date_y', axis= 1, inplace =True)


#OUTPUT
final.to_csv(r"./Output/karaoke.csv", index= False)