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


# MySQL Database Configuration
database_config = {
    'host': 'localhost',
    'user': 'xavier',
    'password': 'Xavier_012',
    'database': 'dogDatabase'
}

topic = "node2_subscribe"

def customCallback(client, userdata, message):
    data = message.split(",")
    breakInFront = emergency_states[0]
    breakInBack = emergency_states[1]
    smokeDetector = emergency_states[2]
    patrolDog = emergency_states[3]
    stopDog = emergency_states[4]
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO Subscribe (breakInFront, breakInBack, smokeDetector, patrolDog, stopDog) VALUES (%s, %s, %s, %s. %s)"
    val = (breakInFront, breakInBack, smokeDetector, patrolDog, stopDog)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

while True:
    myMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(1)
