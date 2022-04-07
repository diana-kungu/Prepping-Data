[**Week 14**](https://preppindata.blogspot.com/2022/04/2022-week-14-house-of-games-winners.html)


**Requirements**
- Input the data
- Only keep relevant fields and rename certain fields to remove duplication
   - Ser. becomes Series
   - Wk. becomes Week
   - T becomes Tu
   - T 1 becomes Th
   - Total becomes Score
   - Week becomes Points
   - Week 1 becomes Rank
- Filter the data to remove Series that have a null value, or are preceded by an 'N'
- Calculate the Points without double points Friday
   - Rank the players based on this new field
   - Create a field to determine if there has been a change in winner for that particular Series and Week
- Rank the players based on their Score instead
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Calculate the Score if the score on Friday was doubled (instead of the Points)
    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Remove unnecessary fields
- Output the data