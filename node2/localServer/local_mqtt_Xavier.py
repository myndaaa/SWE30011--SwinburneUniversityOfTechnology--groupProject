import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import mysql.connector

#Connect to node3 database
mydb = mysql.connector.connect(host="localhost", user="xavier", password="Xavier_012", database="dogDatabase")
#Get the latest entry in the publish table
previous = 0
mycursor = mydb.cursor()
sql = "SELECT id FROM Publish ORDER BY id DESC LIMIT 1"
mycursor.execute(sql)
latest = mycursor.fetchone()
mycursor.close()

if latest != None:
    previous = latest[0]

def on_connect(client, userdata,flags,rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/breakInBack/data")
    client.subscribe("/breakInFront/data")
    client.subscribe("/buzzer/data")
    client.subscribe("/smokeDetector/data")
    
def on_message(client, userdata,msg):
    print(msg.topic + "" + str(msg.payload))
    
    if(msg.topic == "/breakInFront/data"):
        sql ="UPDATE Subscribe SET breakInFront = %s WHERE id ='1'"
        val = (msg.payload)
    elif(msg.topic == "/breakInBack/data"):
        sql ="UPDATE Subscribe SET breakInBack = %s WHERE id ='1'"
        val = (msg.payload)
    elif(msg.topic == "/buzzer/data"):
        sql ="UPDATE Subscribe SET dogState = %s WHERE id ='1'"
        val = (msg.payload)
    elif(msg.topic == "/smokeDetector/data"):
        sql ="UPDATE Subscribe SET smokeDetector = %s WHERE id ='1'"
        val = (msg.payload)
    else:
        print("Error")
        
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
    mycursor.close()
#Function to check if New input is inserted into publish and returns the row
def readPublish():
    mycursor = mydb.cursor()
    sql = "SELECT id, tempValue, humidValue FROM Publish ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    latest = mycursor.fetchone()
    mycursor.close()

    if latest != None and latest[0] != previous:
        return latest
    else:
        return "Clear"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.110",1883,60)
client.loop_forever()
while True:
    #Send data when new input in publish table is detected
    if readPublish() != "Clear":
        message = ""
        data = readPublish()
        tempValue = data[1]
        
        # Publish the message on the "duck" topic to the broker at 192.168.0.102
        publish.single("/tempValue/data", tempValue, hostname="192.168.0.110")