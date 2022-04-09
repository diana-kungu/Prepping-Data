[**Week 9**](https://preppindata.blogspot.com/2022/03/2022-week-9-customer-classifications.html)

**Customer Classification: Cohort Analysis**

**Requirements**
- Input the data
- Aggregate the data to the years each customer made an order
- Calculate the year each customer made their First Purchase
- Scaffold the dataset so that there is a row for each year after a customers First Purchase, even if they did not make an order
- Create a field to flag these new rows, making it clear whether a customer placed an order in that year or not
- Calculate the Year on Year difference in the number of customers from each Cohort in each year
    Cohort = Year of First Purchase
- Create a field which flags whether or not a customer placed an order in the previous year
- Create the Customer Classification using the above definitions
- Join back to the original input data
    - Ensure that in rows where a customer did not place an order, the majority of the original fields are null. The exceptions to this are the Customer Name and Customer ID fields.
- Output the data

