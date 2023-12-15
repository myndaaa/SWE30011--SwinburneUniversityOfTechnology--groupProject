import paho.mqtt.client as mqtt
import time
import mysql.connector

#Connect to node4 database
mydb = mysql.connector.connect(host="localhost", user="pi", password="199412345ItSfYwI", database="node4")

topic = "node4_subscribe"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("/breakinFront/data", "blindFrontState/data", "/fanOn/data")
    
def on_message(client, userdata, msg):
    print(msg.topic + "" +str(msg.payload))
    client.publish("/breakinFront/data")

def customCallback(client, userdata, message):
    data = message.split(",")
    temp = data[0]
    blinds = data[1]
    blindsMode = data[2]
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO subscribe (temp, blinds, blindsMode) VALUES (%s, %s, %s)"
    val = (temp, blinds, blindsMode)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    
broker = mqtt.Client()

broker.on_connect = on_connect
broker.on_message = customCallback

broker.connect("192.168.0.110",1883,60)

broker.loop_forever()
broker.loopforever()
