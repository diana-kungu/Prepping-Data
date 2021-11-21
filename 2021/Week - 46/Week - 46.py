
# IMPORT LIBRARIES
from pandas import ExcelFile, concat, merge, read_csv, read_excel, to_datetime

#READ DATA
#............................................................
with ExcelFile(r'.\Data\Bookshop.xlsx') as xl:
    #Union all the Sales data together to form one row per item in a sale:
    df = concat([read_excel(xl, s) for s in xl.sheet_names if 'Sales' in s])
    #Read all other sheets
    info = read_excel(xl, 'Info', engine='openpyxl')
    awards = read_excel(xl, 'Award')
    checkouts = read_excel(xl, 'Checkouts')
    edition = read_excel(xl, 'Edition')
    publisher = read_excel(xl, 'Publisher')
    ratings = read_excel(xl, 'Ratings')
    series = read_excel(xl, 'Series')
    books = read_excel(xl, 'Book')
    authors = read_excel(xl, 'Author')


#PROCESS DATA
#Change Sale Date field to date
df['Sale Date'] =to_datetime(df['Sale Date'], dayfirst= False)


#Join Books and Author data
book_details = merge(books, authors, how= 'inner')
# Edition
book_details = merge(book_details, edition, how= 'left')

#Add publisher details
book_details = merge(book_details, publisher, how= 'left')

#Add Awards details using Title
#Aggregate Awards per author
awards = awards.groupby('Title', as_index= False)['Award Name'].count().rename(
                                        columns ={'Award Name':'Number of Awards Won'})
book_details = merge(book_details, awards, on= 'Title', how= 'left')

#Add Genre details and Series data

info['BookID'] = info.BookID1  + info.BookID2.astype(str)
info['Staff Comment'] = info['Staff Comment'].str.strip()
#merge Series data
genre_series = merge(info.iloc[:, 2:], series, how= 'left')

#Join genre-series to books details
book_details = merge(book_details, genre_series, how='left')

from numpy import mean

#Agg Ratings
ratings = ratings.groupby('BookID', as_index= False).agg(Average_Rating = ('Rating', 'mean'),
                                             Number_of_Reviewers =('ReviewerID', 'count'), 
                                             Number_of_Reviews =('ReviewID', 'count'))
book_details = merge(book_details, ratings, how='left')

#ADD checkout information
# Aggregate checkout
# - Count the number of months the book has checked out
# - Total Checkouts
checkouts_agg =  checkouts.groupby('BookID', as_index= False).agg(
                                    Total_Checkouts = ('Number of Checkouts', 'sum'),
                                    Number_of_Months_Checked_Out =('CheckoutMonth','count'))
#Merge to books details and checkout data
book_details = merge(book_details, checkouts_agg, how='left')

# Merge to Sales data
orders = merge(df, book_details, how='left')
orders.columns = [c.replace('_', " ") for c in orders.columns]

# Change column type
cols = ['Number of Reviews', 'Total Checkouts', 'Number of Months Checked Out', 'Book Tour Events',\
     'Number of Awards Won', 'Planned Volumes', 'Number of Reviewers', 'Year Established', 'Marketing Spend']
orders[cols] = orders[cols].astype('Int64')

(orders.to_csv('bookshop.csv', index = False))

# %%
#Compare output given and dirived dataframe
data = read_csv(r'.\Output\Week-46-test.csv', engine= 'c', encoding= 'unicode_escape',
 parse_dates=['Sale Date', 'Birthday', 'Publication Date'], dayfirst= True)
data.head()

# OUTPUT
(orders.to_csv(r'.\Output\bookshop.csv', index = False))
print('End')



