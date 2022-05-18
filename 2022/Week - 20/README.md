[**Week 20**](https://preppindata.blogspot.com/2022/05/2022-week-20-tc22-session-attendance.html)

USE CASE: Joins With Exclusion

**Requirements**

- Input the data
- In the Registrations Input, tidy up the Online/In Person field 
- From the Email field, extract the company name
    - We define the company name as being the text following the @ symbol, up to the .
- Count the number of sessions each registered person is planning to attend
- Join on the Session Lookup table to replace the Session ID with the Session name
- Join the In Person/Online Attendees datasets to the cleaned Registrations and only return the
 names of those that did not attend the sessions they registered for.
- Union together these separate streams to get a complete list of those
 who were unable to attend the sessions they registered for.
- Count the number of sessions each person was unable to attend.
- Calculate the % of sessions each person was unable to attend.
    - Round this to 2 decimal places