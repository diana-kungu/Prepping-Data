[**Week 5**](https://preppindata.blogspot.com/2022/02/2022-week-5-prep-school-setting-grades.html)

Use case: Binning, aggregating data

**Requirements**

- Input the data
- Divide the students grades into 6 evenly distributed groups (have a look at 'Tiles' functionality in Prep)
    By evenly distributed, it means the same number of students gain each grade within a subject
- Convert the groups to two different metrics:
    - The top scoring group should get an A, second group B etc through to the sixth group who receive an F
    - An A is worth 10 points for their high school application, B gets 8, C gets 6, D gets 4, E gets 2 and F gets 1.
- Determine how many high school application points each Student has received across all their subjects 
- Work out the average total points per student by grade 
    - ie for all the students who got an A, how many points did they get across all their subjects
- Take the average total score you get for students who have received at least one A and remove anyone who scored less than this. 
- Remove results where students received an A grade (requirement updated 2/2/22)
- How many students scored more than the average if you ignore their As?
- Output the data