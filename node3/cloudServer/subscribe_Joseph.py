from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import mysql.connector

#Establish AWS MQTT Connection
myMQTTClient=AWSIoTMQTTClient("breadBoardWarrior_broker")
myMQTTClient.configureEndpoint("a3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem","/home/pi/certs/77b7e291cd7be423744f6e36403a28e455006e40cb50b73d5baef224267592be-private.pem.key","/home/pi/certs/77b7e291cd7be423744f6e36403a28e455006e40cb50b73d5baef224267592be-certificate.pem.crt" )
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(5)
myMQTTClient.configureMQTTOperationTimeout(10)
myMQTTClient.connect()

#Connect to node3 database
mydb = mysql.connector.connect(host="localhost", user="pi", password="Fruitypebbles", database="node3")

topic = "node3_subscribe"

def customCallback(client, userdata, message):
    data = message.split(",")
    smoke = data[0]
    blinds = data[1]
    blindsMode = data[2]
    
    mycursor = mydb.cursor()
    sql = "UPDATE subscribe SET smoke = %s, blinds = %s, blindsMode = %s"
    val = (smoke, blinds, blindsMode)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

while True:
    myMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(1)
