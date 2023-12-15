import serial
import time
import mysql.connector

#Connect to node4 database and create publish and subscribe tables
mydb = mysql.connector.connect(host="localhost", user="pi", password="199412345ItSfYwI", database="node4")

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS publish(id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, door BOOLEAN, breakIn BOOLEAN)")
mycursor.execute("CREATE TABLE IF NOT EXISTS subscribe(id INT AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, temp BOOLEAN, blinds INT, blindsMode BOOLEAN)")
mycursor.close()

#Get previous id for comparison defaults to 0 if no data
previous = 0
mycursor = mydb.cursor()
sql = "SELECT id FROM subscribe ORDER BY id DESC LIMIT 1"
mycursor.execute(sql)
latest = mycursor.fetchone()
mycursor.close()

if latest != None:
    previous = latest[0]

#Open the Serial connection to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

#Function to detect when new input is inserted into subscribe table and returns the row
def readSubscribe():
    mycursor = mydb.cursor()
    sql = "SELECT id, temp , blinds, blindsMode FROM subscribe ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    latest = mycursor.fetchone()
    mycursor.close()

    if latest != None and latest[0] != previous:
        return latest
    else:
        return "Clear"
    
#function to Insert data into publish table    
def writePublish(door, breakIn):
    mycursor = mydb.cursor()
    sql = "INSERT INTO publish (door, breakIn) VALUES (%s, %s)"
    val = (door, breakIn)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

#Global variables for blinds settings and position
mode = 0
blindsPos = 0
temp1 = 24.0

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
    if readSubscribe() != "Clear":
        subscribe = readSubscribe()
        temp = subscribe[1]
        blinds = subscribe[2]-1
        blindMode = subscribe[3]
        
        #Set blinds mode to new setting
        mode = blindMode
        temp1 = temp
        
        
        #Append blinds destination into the message based on manual or automatic mode
        if mode:
            message += blinds
            blindsPos = blinds
        else:
            if light > 300:
                blindsPos = 5
                message += "5,"
            elif light >200:
                blindsPos = 2
                message += "2,"
            else:
                blindsPos = 0
                message += "0,"
                
        
    else:
        #Do the same message for no new input but using global variables
        if mode:
            message += blindsPos + ","
        else:
            if light > 300:
                blindsPos = 5
                message += "5,"
            elif light >200:
                blindsPos = 2
                message += "2,"
            else:
                blindsPos = 0
                message += "0,"
            
    if temp1 > 26:
                message += "1,"
    else:
                temp = 2
                message += "0,"
    ser.write(bytes(message,"utf-8"))
    print(read_serial)
    print(message)

    
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