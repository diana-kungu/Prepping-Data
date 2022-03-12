# 
#Import Libraries
from pandas import ExcelFile, read_excel
from collections import Counter
from numpy import prod


#Load Data
with ExcelFile(r'.\2022\Week - 6\Input\7 letter words.xlsx') as xl:
    words = read_excel(xl, '7 letter words')
    scores = read_excel(xl, 'Scrabble Scores')
    
#Process Data
#Parse out the information in the Scrabble Scores Input so that there are 3 fields: 
# Tile/Frequency/ Points
scores[['Points', 'Tiles']] = scores['Scrabble'].str.split(':', expand = True)
scores.drop('Scrabble', axis=1, inplace= True)
scores['Tiles'] = scores['Tiles'].str.split(',')
scores = scores.explode('Tiles')
scores[['Tiles', 'frequency']] = scores['Tiles'].str.split('×', expand = True)
scores['Points'] = [int(x[0]) for x in scores['Points'].str.split(" ")]
#Format and clean columns
scores.frequency = scores.frequency.astype('int')
scores['Tiles'] = scores['Tiles'].str.strip()

#Calculate the % Chance of drawing a particular tile
scores['% chance'] =(scores['frequency']/sum(scores['frequency'])).round(2)

# Create frequency, points & % chance dictionaries
freq_dict = dict(zip(scores['Tiles'][1:].str.lower(), scores['frequency'][1:]))
points_dict = dict(zip(scores['Tiles'][1:].str.lower(), scores['Points'][1:]))
prob_dict = dict(zip(scores['Tiles'][1:].str.lower(), scores['% chance'][1:]))

# Split each of the 7 letter words into individual letters and count the number
# of occurrences of each letter
words['letter'] =[list(x.lower()) for x in words['7 letter word']]
words['Count'] = words['letter'].apply(lambda x: Counter(x))

# Filter out words with a 0% chance
words['no chance'] = words['Count'].apply(lambda d: any([1 for key in d.keys()
                                                     if d[key] > freq_dict[key] ]))
words = words[words['no chance'] != True].copy()

# Calculate the total points each word would score
#Calculate the total % chance of drawing all the tiles necessary to create each word
words['Total Points'] = words['Count'].apply(lambda d: sum([d[key]* points_dict[key] 
                                                      for key in d.keys()]))
words['% Chance'] = words['Count'].apply(lambda d: float('{:.3g}'.format(prod([prob_dict[key]** d[key]
                                                      for key in d.keys()]))))
# Rank the words by their % chance (dense rank)
#Rank the words by their total points (dense rank)
words['Points Rank'] = words['Total Points'].rank(method='dense', ascending= False).astype('int')
words['Likelihood Rank'] = words['% Chance'].rank(method='dense', ascending= False).astype('int')

words.sort_values(by=['Points Rank'], ascending= True, inplace= True)
words.drop(['letter', 'Count', 'no chance'], axis= 1, inplace= True)


#Output
words.to_csv(r".\2022\Week - 6\Output\scrabble.csv", index= False)
print('End')

