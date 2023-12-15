from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import mysql.connector

#Establish AWS MQTT Connection
myMQTTClient = AWSIoTMQTTClient("breadBoardWarrior_broker")
myMQTTClient.configureEndpoint("aa3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem","/home/pi/certs/a930561b2de9982470b484e2f703450c0e76ff33b751af3b7506d300a9121f55-private.pem.key","/home/pi/certs/a930561b2de9982470b484e2f703450c0e76ff33b751af3b7506d300a9121f55-certificate.pem.crt" )
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(5)
myMQTTClient.configureMQTTOperationTimeout(10)
myMQTTCLIENT.connect()

#Connect to node4 database
mydb = mysql.connector.connect(host="localhost", user="pi", password="199412345ItSfYwI", database="node4")

topic = "node4_subscribe"

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

while True:
    myMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(1)