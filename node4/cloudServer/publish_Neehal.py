from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import mysql.connector




#Establish AWS MQTT connection
myMQTTClient = AWSIoTMQTTClient("breadBoardWarrior_broker")
myMQTTClient.configureEndpoint("aa3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/AmazonRootCA1.pem","/home/pi/certs/a930561b2de9982470b484e2f703450c0e76ff33b751af3b7506d300a9121f55-private.pem.key","/home/pi/certs/a930561b2de9982470b484e2f703450c0e76ff33b751af3b7506d300a9121f55-certificate.pem.crt" )
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(4)
myMQTTClient.configureMQTTOperationTimeout(5)

myMQTTClient.connect()

#Connect to node4 database
mydb = mysql.connector.connect(host="localhost", user="pi", password="199412345ItSfYwI", database="node4")
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

while True:
    #Send data when new input in publish table is detected
    if readPublish() != "Clear":
        message = ""
        data = readPublish()
        
        #Convert tuple data into string seperated by ","
        for x in range(2) :
            message += str(data[x]) + ","
        message += str(data[3])
        
    myMQTTClient.publish("node4_publish", message, 0)