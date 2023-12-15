import time
import mysql.connector
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# The callback for when the client receivesa CONNACK response from the server.
def on_connect(client,userdata,flags,rc):
    print("Connected with result code " + str(rc))
    #Subscribing in on_connect() means that if we lose the connection and
    #reconnect then subscriptions will be renewed
    client.subscribe("exhaustOn/data")
    client.subscribe("blindBack/data")
    client.subscribe("blindBackState/data")

# The callback for when a PUBLISH message is received from the server.
def on_message(client,userdata,msg):
    print(msg.topic+ " " + str(msg.payload))
    
    if (msg.topic == "exhaustOn/data"):
        sql = "UPDATE subscribe SET smoke = $s WHERE id = '1'"
        val = (msg.payload)
    elif (msg.topic == "blindBack/data"):
        sql = "UPDATE subscribe SET blinds = $s WHERE id = '1'"
        val = (msg.payload)
    elif((msg.topic == "blindBackState/data")):
        sql = "UPDATE subscribe SET blindsMode = $s WHERE id = '1'"
        val = (msg.payload)
    else:
        print("Error")
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a manual interface.

#Connect to node3 database
mydb = mysql.connector.connect(host="localhost", user="pi", password="Fruitypebbles", database="node3")
#Get the latest entry in the publish table
previous = 0
mycursor = mydb.cursor()
sql = "SELECT id FROM publish ORDER BY id DESC LIMIT 1"
mycursor.execute(sql)
latest = mycursor.fetchone()
mycursor.close()

if latest != None:
    previous = latest[0]

#Function to check if New input is inserted into publish and returns the row
def readPublish():
    mycursor = mydb.cursor()
    sql = "SELECT id, timestamp, door, breakIn FROM publish ORDER BY id DESC LIMIT 1"
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
        doorBack = data[2]
        breakInBack = data[3]
        #Convert tuple data into string seperated by ","

    publish.single("doorBack/data",doorBack,hostname="192.168.0.110")
    publish.single("breakInBack/data",breakInBack,hostname="192.168.0.110")

    