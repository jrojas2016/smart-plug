import sqlite3
import time

# Create a connection and cursor with the DB
dbConnection = sqlite3.connect('Data.db')
dbCursor = dbConnection.cursor()

# Create table
# dbCursor.execute("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)")

# dbCursor.execute("DELETE FROM stocks") # DELETE all content in the TABLE

# # Insert a row of data
# dbCursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# # Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#             ]
# dbCursor.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

sTime = time.time() # Seconds since EPOCH
sTimeStamp = (sTime,) # To avoid HACKERS

# # Insert a row of data
dbCursor.execute("INSERT INTO stocks VALUES (?,'BUY','RHAT',100,35.14)", sTimeStamp)

# Save (commit) the changes
dbConnection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
dbConnection.close()


