# prepping week 22
#Load modules
from pandas import read_excel, ExcelFile, merge, concat


#Read data
with ExcelFile(r'.\2022\Week - 22\Input\Critical_Role_Campaign_1_Datapack.xlsx') as  xl:
    dialogue = read_excel(xl, sheet_name = 'dialogue' )
    episode = read_excel(xl, sheet_name = 'episode_details' )

# PROCESSING
#Merge dialogue amd episode details df to obtain the runtime of each episode
df = dialogue.merge(episode.loc[:, ['Episode', 'runtime_in_secs']])
# Extract the Last character from each episode and assign time_in_sec == runtime_in_secs
# to find the end of converstion
last = df.iloc[df.groupby(['Episode']).time_in_secs.idxmax(), :].copy()
last['time_in_secs'] = last['runtime_in_secs']

#combine dialogue df with last character dialogue
df = concat([df, last], ignore_index= True)
#Some character names are comma separated, split these names out and trim any trailing whitespace
df = df.assign(name=df.name.str.split(", ")).explode("name")

#Create a rank of the timestamp for each episode, ordered by earliest timestamp
df['timestamp_ranks'] = df.groupby(['Episode'])['time_in_secs'].rank(method='dense').astype(int)
df['end_time_in_sec'] = df['timestamp_ranks']+1

duration = []
def rec_shift(gp, i, j):
        '''recursive function that get the difference between two concecutive row
        if they are not equal, otherwise move to the next row
        '''
        try:
                if gp['time_in_secs'].iloc[i] != gp['time_in_secs'].iloc[j]:
                        duration.append(gp['time_in_secs'].iloc[j] - gp['time_in_secs'].iloc[i])
                
                
                if gp['time_in_secs'].iloc[i] == gp['time_in_secs'].iloc[j]:
                        rec_shift(gp, i, j+1)
        except:
                duration.append('null') 
       
# Sort dataframe
df.sort_values(by=['Episode', 'timestamp_ranks'], inplace= True)

#Calculate the dialogue durations
for n, gp in df.groupby('Episode'):
    for i, j in enumerate(range(len(gp))):
        rec_shift(gp, i, j+1)
df['duration'] = duration

#Filter the data for just Gameplay sections
df = df[(df['duration'] != 'null') & (df['section']=='Gameplay')]

#Remove duplicates
df.drop_duplicates(inplace=True)

#OUTPUT
cols = ['Episode', 'name', 'time_in_secs', 'duration', 'youtube_timestamp',
        'dialogue', 'section']
df.to_csv(r'.\2022\Week - 22\Output\critical_game.csv', columns=cols,
          index=False)

print('prepped!')
