import serial
import time
import mysql.connector

# Connect to database
mydb = mysql.connector.connect(host="localhost", user="xavier", password="Xavier_012", database="dogDatabase")



# Create tables if it doesn't exist yet
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Publish(id INT AUTO_INCREMENT PRIMARY KEY, tempValue FLOAT, humidValue FLOAT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Subscribe(id INT AUTO_INCREMENT PRIMARY KEY, breakInFront BOOLEAN, breakInBack BOOLEAN, smokeDetector BOOLEAN, patrolDog BOOLEAN, stopDog BOOLEAN)")
mycursor.close()

ser = serial.Serial('/dev/ttyUSB0', 9600)

# Function to write into subscribe database
def readSubscribe():
    mycursor = mydb.cursor()
    sql = "SELECT id, breakInFront, breakinBack, smokeDetector, dogState FROM Subscribe ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    latest = mycursor.fetchone()
    mycursor.close()
    
    return latest

#  Function to write into publish database
def writePublish(tempValue, humidValue):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Publish (tempValue, humidValue) VALUES (%s, %s)"
    val = (tempValue, humidValue)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    
# Running on loop
while True:
    read_serial = ser.readline().decode("utf-8").strip()
    data = read_serial.split(":")
    
    tempValue = data[0]
    humidValue = data[1]
    
    writePublish(tempValue, humidValue)
    
    if readSubscribe() != None:
        subscribe = readSubscribe()
        breakInFront = subscribe[1]
        breakinBack = subscribe[2]
        smokeDetector = subscribe[3]
        patrolDog = subscribe[4]
        stopDog = subscribe[5]
    
    message = ""
    
    if breakInFront or breakinBack or smokeDetector == 1 :
        message += "6"
    elif patrolDog == 1:
        message += "3"
    elif stopDog == 1:
        message+= "4"
    else:
        message += "0"
        
    ser.write(message)
