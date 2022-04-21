[**Week 16**](https://preppindata.blogspot.com/2022/04/2022-week-16-restaurant-orders.html)

use case: Unstructured Excel file

**Requirements**
- Input the data
- Reshape the Orders table so that we have 3 columns:
    Guest name
    Dish
    Selections (containing 🗸 or null)
- Extract the course name from the Dish field
    Group these so that Starter and Starters are treated the same, for example
- Fill down the course name for each Guest (hint)
    It may help to bring in the Recipe ID from the Lookup Table 
- Filter out where the Dish = Course
- Filter out Dishes which have not been selected
- Output the Data