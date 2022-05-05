[**Week 17**](https://preppindata.blogspot.com/2022/04/2022-week-17-price-of-streaming.html)

Use Case: Joing datasets which have different levels of aggregation.

**Requirements**
- Input the data
- Check the location field for spelling errors
- Fix the date fields so they are recognised as date data types
- Aggregate the data to find the total duration of each streaming session (as identified by the timestamp)
- Update the content_type field:
    - For London, Cardiff and Edinburgh, the content_type is defined as "Primary"
    - For other locations, maintain the "Preserved" content_type and update all others to have a "Secondary" content_type
- Update Avg Pricing field
    - For "Primary" content, we take the overall minimum streaming month, ignoring location
    - For all other content, we work out the minimum active month for each user, in each location and for each content_type
- For "Preserved" content, we manually input the Avg Price as £14.98
- Output the data