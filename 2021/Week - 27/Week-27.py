# IMPORTS
from pandas import ExcelFile, read_excel, melt, merge, DataFrame
from random import choices
from scipy.stats import mode

# Read Data
with ExcelFile(r'.\Data\PD 2021 Wk 27 Input.xlsx') as xl :
    seeding = read_excel(xl, sheet_name = 'Seeding' )
    teams = read_excel(xl, sheet_name= 'Teams')


# Process Data
#.....................................................................................
#Melt seeding dataframe and clean probabilities column
df =melt(seeding, id_vars='Seed', var_name='Pick', value_name='Probability').dropna()
df['Probability'] = df['Probability'].astype('str').str.strip('>').astype('float')/100

# Set seed to index
df.set_index('Seed', drop=True, inplace = True)

# Function that generates a list of weighted random number, then the 
# most frequent number is selected;
# n- number of iteration(numbers generated)
# p - Weights(probability of each Seed)
# s - list of Seed to be selected from
def lottery(n,s,p):
    lst = []
    for i in range(n):
        lst.append(choices(s,p, k=1)[0])

    most_freq_val = lambda x: mode(x)[0][0]  
    d = most_freq_val(lst)
    return d

# Generate a list with the first four weighted random Seeds then add all numbers 
# in 1-14 range that are not in the weighted list
seeding = []
for i in range(14):
    if len(seeding)<4:
        try:
            #Drop all seeds that most recent Seed selected
            df.drop(seeding[-1], axis=0, inplace= True)
        
            temp = df[df['Pick'] == i+1] #Pick nos. 
            s = temp.index #Seeds to select from
            p = temp.Probability # Weight of each Seed
            draw = lottery(1000, s, p)
            seeding.append(draw)
                      
        except:
            temp = df[df['Pick'] == i+1]
            s = temp.index
            p = temp.Probability
            draw = lottery(1000, s, p)
            seeding.append(draw)
            
    else:
        seeding.extend([i for i in range(1,15) if i not in seeding])

# Create a dataframe with Seed list obtain above
# Merge with team data
lott_results = DataFrame(seeding, columns=['Seed'])
lott_results = merge(lott_results, teams, how='left',on='Seed')
lott_results = lott_results.reset_index().rename(columns={'index': 'Actual Pick'})
lott_results['Actual Pick'] = lott_results['Actual Pick'].apply(lambda x: x+1)
lott_results.rename(columns={'Seed': 'Original'}, inplace=True)
#..................................................................................................


#OUTPUT
lott_results.to_csv(r'./Output/week27.csv', index=0)
print('End')


