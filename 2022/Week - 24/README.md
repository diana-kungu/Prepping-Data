[**Week**](https://preppindata.blogspot.com/2022/06/2022-week-24-longest-flights.html)

Use cases: Merge dataframes, Parsing Text with Regex

Requirements
- Remove the airport names from the From and To field

- Create a Route field which concatenates the From and To fields with a hyphen
    e.g. Dubai - Dallas

- Split out the Distance field so that we have one field for the Distance in km and one field for the Distance in miles
    Ensure these fields are numeric

- Rank the flights based on Distance
- The Scheduled duration is a Date/Time data type. Change this to a string so that we only keep the time element
- Update the First flight field to be a date
- Join on the lat & longs for the From and To cities