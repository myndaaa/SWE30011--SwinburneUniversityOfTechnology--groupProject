import serial
import mysql.connector

#  MariaDB connection 
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "localdb"

 # Connect to MariaDB
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

cursor = db_connection.cursor()   
ser = serial.Serial('/dev/ttyS0', 9600)  

while True:
    # Read data from the serial monitor
    data = ser.readline().decode().strip().split(',')

    if len(data) == 5:
        temperature, mappedMoisture, smoke, waterLevelState, rainValue = map(float, data)

        # Insert data into the corresponding tables
        cursor.execute("INSERT INTO dht11 (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
        cursor.execute("INSERT INTO soil (mappedMoisture) VALUES (%s)", (mappedMoisture,))
        cursor.execute("INSERT INTO smoke (smoke) VALUES (%s)", (smoke,))
        cursor.execute("INSERT INTO waterlevel (waterlevelstate) VALUES (%s)", (waterLevelState,))
        cursor.execute("INSERT INTO rain (rainvalue) VALUES (%s)", (rainValue,))

        # Commit 
        db_connection.commit()

# Close when  interrupted
cursor.close()
db_connection.close()