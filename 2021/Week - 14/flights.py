#IMPORTS
from pandas import read_excel, ExcelFile, DataFrame, merge, to_datetime
from os import chdir
from numpy import select, where

chdir(r'C:\Users\DIANA\Desktop\Prepping_data')

#Read Excels file Data
with ExcelFile(r".\Data\Week 14 - Input.xlsx") as xl:
    pass_ = read_excel(xl, 'Passenger List')
    seats = read_excel(xl, 'SeatList')
    flights = read_excel(xl, 'FlightDetails')
    planes = read_excel(xl, 'PlaneDetails')


#Process Data
# Parse Seats Details
seats.set_index('Row', inplace= True)
row = seats.index.repeat(6)
seats = seats.astype('str')
seats_nos = (seats.values + seats.columns.values).flatten()
#Create new Seats dataframe
seats = DataFrame(seats_nos, columns=['Seat No.'])
seats['passenger_number'] = seats['Seat No.'].str.slice(0,-1)
seats['Row'] =row
# Seat Type
conditions = [(seats['Seat No.'].str.slice(-1) == 'A') | (seats['Seat No.'].str.slice(-1) == 'F'),\
             (seats['Seat No.'].str.slice(-1) == 'B') | (seats['Seat No.'].str.slice(-1) == 'E'),\
            (seats['Seat No.'].str.slice(-1) == 'C') | (seats['Seat No.'].str.slice(-1) == 'D')]
choices = ['Window seat', 'Middle seat', 'Aisle seats']

seats["Seat Type"] = select(conditions, choices)

#Combine Seat and passenger details dataframe
pass_.flight_number = pass_.flight_number.astype(str)
seats.passenger_number =seats.passenger_number.astype(str)
pass_.passenger_number =pass_.passenger_number.astype(str)
pass_ = pass_.merge(seats, how= 'left' )

#Parse Flights details 
cols = flights.columns[0][1:-1].split('|')
flights = DataFrame(flights['[FlightID|DepAir|ArrAir|DepDate|DepTime]'].str.slice(1,-1).str.split('|',\
                    expand= True).values, columns= cols)
#Time of day departure
flights.DepTime = to_datetime(flights.DepTime)
flights["Time of day"] = where(flights.DepTime < '12:00:00', 'Morning',\
                        where((flights.DepTime >= '12:00:00' ) & (flights.DepTime <= '18:00:00' ), 'Afternoon',\
                        'Evening'))

#Parse Planes Data
planes['Business Class'] = [[i for i in range(1, int(planes['Business Class'][j][2:])+1)]\
                                for j in range(len(planes))]
business_class_dict = dict(zip(planes['FlightNo.'], planes['Business Class']))

#Create a Seat Class(Economy vs Business Class) field in the Passenger dataframe
pass_['Seat Class'] = ['Business Class' if int(pass_['Row'][i]) in\
             business_class_dict.get(int(pass_['flight_number'][i]))\
                 else 'Economy' for i in range(len(pass_))]

#Merge Passenger and flights details tables
combined = pass_.merge(flights, how= 'left', left_on= 'flight_number', right_on= 'FlightID')

#Q1 What time of day were the most purchases made? (Avg per flight)
q1 = combined[combined['Seat Class'] != 'Business Class'].groupby(['FlightID', 'Time of day'])\
            ['purchase_amount'].sum().groupby('Time of day').mean().reset_index()\
                .sort_values(by= 'purchase_amount', ascending = False )
q1['purchase_amount'] = q1['purchase_amount'].round(2)
q1.rename(columns={'purchase_amount': 'Avg amount'}, inplace= True)
q1['Rank'] = q1['Avg amount'].rank(method= 'dense', ascending= False).astype(int)

#Q2 What seat position had the highest purchase amount?
q2 = combined[combined['Seat Class'] != 'Business Class'].groupby(['Seat Type'])['purchase_amount'].sum()\
                        .reset_index().sort_values(by= 'purchase_amount', ascending = False )
q2['Rank'] = q2['purchase_amount'].rank(method= 'dense', ascending= False).astype(int)

#Q3 Business class purchases are free. How much is this costing us?
q3 = combined.groupby(['Seat Class'])['purchase_amount'].sum()\
                        .reset_index().sort_values(by= 'purchase_amount', ascending = False )
q3['Rank'] = q3['purchase_amount'].rank(method= 'dense', ascending= False).astype(int)


#OUTPUT
q1.to_csv(r'.\Output\q1.csv', index = False)
q2.to_csv(r'.\Output\q2.csv', index = False)
q3.to_csv(r'.\Output\q3.csv', index = False)