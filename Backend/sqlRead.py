import sqlite3

# Create a connection and cursor with the DB
dbConnection = sqlite3.connect("C:\Users\Robotics.Phd\.ssh\Documents\DataBases\SmartPlugData.db")
dbCursor = dbConnection.cursor()

##### Never do this -- insecure! ####
# symbol = 'RHAT'
# dbCursor.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('0',)
dbCursor.execute('SELECT * FROM rawData WHERE device_id=?', t)
#print dbCursor.fetchone()
print dbCursor.fetchall()

dbConnection.close()