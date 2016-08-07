import sqlite3 # Database interface

# Create a connection and cursor with the DB
dbConnection = sqlite3.connect("C:\Users\Robotics.Phd\.ssh\Documents\DataBases\SmartPlugData.db")
dbCursor = dbConnection.cursor()

# DELETE all content in the TABLE
#dbCursor.execute("DELETE FROM rawData") 

# REMOVE TABLE completely
dbCursor.execute("DROP TABLE rawData") 

# Create table
dbCursor.execute("CREATE TABLE rawData (timestamp, device_id, device_state, device_event, voltage, current, power, app_id, app_state, app_event)")

# Save (commit) the changes
dbConnection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
dbConnection.close()