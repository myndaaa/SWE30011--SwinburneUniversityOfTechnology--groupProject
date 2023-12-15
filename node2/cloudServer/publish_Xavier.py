from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import mysql.connector

myMQTTClient = AWSIoTMQTTClient("breadBoardWarrior_broker")
myMQTTClient.configureEndpoint("a3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/xavier/certs/AmazonRootCA1.pem","/home/xavier/certs/38e2da1856e78ba7e946736d4e5d22a5fa679fcd629b2e90c302eed1684cb8c7-private.pem.key","/home/xavier/certs/38e2da1856e78ba7e946736d4e5d22a5fa679fcd629b2e90c302eed1684cb8c7-certificate.pem.crt" )
myMQTTClient.configureOfflinePublishQueueing(-1)  
myMQTTClient.configureDrainingFrequency(5)  
myMQTTClient.configureConnectDisconnectTimeout(5)  
myMQTTClient.configureMQTTOperationTimeout(10)
myMQTTClient.connect()

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

while True:
    #Send data when new input in publish table is detected
    if readPublish() != "Clear":
        message = ""
        data = readPublish()
        
        #Convert tuple data into string seperated by ","
        for x in range(2) :
            message += str(data[x]) + ","
        message += str(data[3])
        
        myMQTTClient.publish("node2_publish", message, 0)
