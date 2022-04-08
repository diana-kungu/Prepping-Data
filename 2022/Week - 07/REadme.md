[**Week 7**](https://preppindata.blogspot.com/2022/02/2022-week-7-call-center-agent-metrics.html)

**Requirements**
- Input the data
- People, Location, Leader, and Dates:
   - Join the People, Location, and Leader data sets together
   - Remove the location id fields, the secondary leader id field
   - Create last name, first name fields for the agent and the leader
   - Limit the dates to just 2021 and join those to the People, Location, Leader step
   - Keep the id, agent name, leader 1, leader name, month start date, join, and location field
- Monthly Data
   - union the worksheets in the input step
   - merge the mismatched fields
   - create a month start date
   - remove the table names and file paths field
   - join the data with the people - remember we need to show every agent for every month
- Goals
   - add the goals input to the flow
   - clean the goal data to have the goal name & numeric value
   - add the goals to the combined people & data step be sure that you aren't increasing the row count - the goals should be additional columns
- Metrics & Met Goal Flags
   - create a calculation for the percent of offered that weren't answered (for each agent, each month)
   - create a calculation for the average duration by agent (for each agent, each month)
   - create a calculation that determines if the sentiment score met the goal
   - create a calculation that determines if the not answered percent met the goal
- Output the data