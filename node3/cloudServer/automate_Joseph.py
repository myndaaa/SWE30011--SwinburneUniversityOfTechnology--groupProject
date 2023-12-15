import serial
import time
import mysql.connector

#Connect to node3 database and create publish and subscribe tables
mydb = mysql.connector.connect(host="localhost", user="pi", password="Fruitypebbles", database="node3")

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS publish(id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, door BOOLEAN, breakIn BOOLEAN)")
mycursor.execute("CREATE TABLE IF NOT EXISTS subscribe(id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, smoke BOOLEAN, blinds INT, blindsMode BOOLEAN)")
mycursor.close()

#Open the Serial connection to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

#Function to detect when new input is inserted into subscribe table and returns the row
def readSubscribe():
    mycursor = mydb.cursor()
    sql = "SELECT id, smoke , blinds, blindsMode FROM subscribe ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    latest = mycursor.fetchone()
    mycursor.close()

    return latest
    
#function to Insert data into publish table    
def writePublish(door, breakIn):
    mycursor = mydb.cursor()
    sql = "INSERT INTO publish (door, breakIn) VALUES (%s, %s)"
    val = (door, breakIn)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

#Global variables for allowing publish to prevent spamming
publishDoor = False
publishBreak = False    
while True:
    #Get string from Arduino and seperate them into 3 variables
    read_serial = ser.readline().decode("utf-8").strip()
    data = read_serial.split(":")
    light = int(data[0])
    door = int(data[1])
    breakIn = int(data[2])
    
    message = ""
    #Test if new input is found in subscribe table, If so, send message based on new inputs
    subscribe = readSubscribe()
    smoke = subscribe[1]
    blinds = subscribe[2] - 1
    blindsMode = subscribe[3]
        
    #Set blinds mode to new setting
    mode = blindsMode
        
    #Append blinds destination into the message based on manual or automatic mode
    if mode:
        message += blinds
    else:
        if light > 300:
            message += "2,"
        elif light >200:
            message += "1,"
        else:
            message += "0,"
                
    #Append smoke boolean to the message    
    message += smoke
        
    print(read_serial)
    print(message)
    ser.write(bytes(message, "utf-8"))
    
    #Publish data when door or breakIn happens
    if breakIn and not publishBreak:
        publishBreak = True
        writePublish(door, breakIn)
    elif door and not publishDoor:
        publishDoor = True
        writePublish(door, breakIn)
        
    if not breakIn and publishBreak:
        publishBreak = False
    elif not door and publishDoor:
        publishDoor = False