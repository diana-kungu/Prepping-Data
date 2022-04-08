[**Week 6**](https://preppindata.blogspot.com/2022/02/2022-week-6-7-letter-scrabble-words.html)

**Requirements**

- Input the data
- Parse out the information in the Scrabble Scores Input so that there are 3 fields:
   - Tile
   - Frequency
   - Points
- Calculate the % Chance of drawing a particular tile and round to 2 decimal places
   - Frequency / Total number of tiles
- Split each of the 7 letter words into individual letters and count the number of occurrences of each letter
- Join each letter to its scrabble tile 
- Update the % chance of drawing a tile based on the number of occurrences in that word
   - If the word contains more occurrences of that letter than the frequency of the tile, set the probability to 0 - it is impossible to make this word in Scrabble
   - Remember for independent events, you multiple together probabilities i.e. if a letter appears more than once in a word, you will need to multiple the % chance by itself that many times
- Calculate the total points each word would score
- Calculate the total % chance of drawing all the tiles necessary to create each word
- Filter out words with a 0% chance
- Rank the words by their % chance (dense rank)
- Rank the words by their total points (dense rank)
- Output the data