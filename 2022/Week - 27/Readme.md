[**Week 27**](https://preppindata.blogspot.com/2022/07/2022-week-27-c-clean-and-aggregate.html)

**Requirements**
- Input the data 
- Separate out the Product Name field to form Product Type and Quantity
    - Rename the fields to 'Product Type' and 'Quantity' respectively
- Create two paths in your flow: 
    One to deal with the data about Liquid Soap sales
    One to deal with the data about Bar Soap sales
- For each path in your flow:
    - Clean the Quantity field to just leave values
        For Liquid, ensure every value is in millilitres 
- Sum up the sales for each combination of Store, Region and Quantity
- Also, count the number of orders that has the combination of Store, Region and Quantity. Name this field 'Present in N orders' 
- Output each file from the separate paths