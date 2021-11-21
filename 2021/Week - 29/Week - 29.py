
#Imports
from pandas import ExcelFile, read_excel, merge, to_datetime, notna
from datetime import datetime
from numpy import where


#Read Data
with ExcelFile(r'.\Data\Olympic Events.xlsx') as xl :
    df = read_excel(xl)
    venue = read_excel(xl, 'Venues')
df.head()

# PROCESS DATA
#Create a correctly formatted DateTime field 
date = df['Date'].str.extract(r'(\d+)(?:\w{2})(_\w+\d{4})')
df['Date'] =date[0]+ date[1]+" "+df['Time']

df['Date'] = to_datetime(df['Date'], format='%d_%B_%Y %H:%M', errors='coerce')
df.Time = df['Date'].dt.strftime('%H:%M') 
df['Date'] = df['Date'].dt.date

#Parse the event list so each event is on a separate row 
df['Events'] = df['Events'].str.split(',')
df = df.explode('Events', ignore_index=1)

#Group similar sports into a Sport Type field
df['Sport'] = df['Sport'].str.strip('.').str.title().str.replace("Bmx", "BMX").str.strip()
#Clean spellings in sports names
df['Sport'] = where(((df['Sport'] == 'Beach Volleybal') | (df['Sport'] == 'Beach Volley')), 'Beach Volleyball',
                where(((df['Sport'] == 'Softball/Baseball') | (df['Sport'] == 'Baseball') |
                (df['Sport'] == 'Softball')), 'Baseball/Softball',
                where((df['Sport'] == '3X3 Basketball'), '3x3 Basketball',
                where((df['Sport'] == 'Artistic Gymnastic'), 'Artistic Gymnastics',
                        df['Sport']))))

# Sport Type grouping
df['Sport Type'] =  where(((df['Sport'] == 'Beach Volleyball') | (df['Sport'] == 'Volleyball')), 'Volleyball', 
         where((df['Sport'] == '3x3 Basketball'), 'Basketball',
        where(((df['Sport'] == 'Baseball/Softball') | (df['Sport'] == 'Softball') |(df['Sport'] == 'Baseball')), 'Baseball/Softball',
        where(((df['Sport'] == 'Cycling Mountain Bike') | (df['Sport'] == 'Cycling Road')
        |(df['Sport'] == 'Cycling BMX Freestyle') |(df['Sport'] == 'Cycling Track')), 'Cycling', 
        where(((df['Sport'] == 'Trampoline Gymnastics' )| (df['Sport'] == 'Artistic Gymnastics')), 'Gymnastics',    
        where(((df['Sport'] == 'Judo') | (df['Sport'] == 'Karate') | (df['Sport'] == 'Taekwondo')), 'Martial Arts',   
        where(((df['Sport'] == 'Canoe Slalom') | (df['Sport'] == 'Canoe Sprint')), 'Canoeing',   
        where(((df['Sport'] == 'Marathon Swimming') | (df['Sport'] == 'Artistic Swimming')), 'Swimming',   
        where((df['Sport'] == 'Fencing'), 'Modern Pentathlon',   df['Sport'])))))))))

# Process venue data
#split location and expand it to obtain Lats and Longitudes
venue[['Latitude', 'Longitude']] =venue['Location'].str.split(',', expand= True)
venue[['Latitude', 'Longitude']] = venue[['Latitude', 'Longitude']].astype('float')
venue.drop('Location', axis=1, inplace= True)
#Remove white spaces in columns
venue.Sport = venue.Sport.str.strip()
df['Venue'] = where((df['Venue'] == 'Fuji international Speedway'), 'Fuji International Speedway', df['Venue'])
#Combine the Venue table to sports table
df_merge = (merge(df, venue, how='left', left_on=['Venue', 'Sport'],
                      right_on=['Venue', 'Sport']))

#Calculate whether the event is a 'Victory Ceremony' or 'Gold Medal' event. 
df_merge['Medal Ceremony?'] = df['Events'].map(lambda x: ('Gold' in x )| ('Victory' in x))


#OUTPUT
df_merge.to_csv(r'.\Output\week29.csv', index = False, encoding = 'utf-8-sig')
print('End')


