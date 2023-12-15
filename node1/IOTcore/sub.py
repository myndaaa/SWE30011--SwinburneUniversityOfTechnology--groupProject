import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("breadBoardWarrior_node1")

myMQTTClient.configureEndpoint("a3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert/AmazonRootCA1.pem", "/home/pi/cert/cb53821e62b7edc905dc7d37abe4d1df422e9e5589666d87c151d683b7c2355d-private.pem", "/home/pi/cert/cb53821e62b7edc905dc7d37abe4d1df422e9e5589666d87c151d683b7c2355d-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

topic = "node1_subscribe"

def customCallback(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    node_data = message.payload.strip()  # Remove leading/trailing whitespaces

    # Local DB connection
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="localdb")
    mycursor = mydb.cursor()

    # Insert data into the 'motorState' table
    try:
        sql = "INSERT INTO motorState (state) VALUES (%s)"
        mycursor.execute(sql, (node_data,))
        mydb.commit()
        print("Data inserted into localdb: motorState")
    except Exception as e:
        print("Error inserting data into localdb:", str(e))
    finally:
        mycursor.close()

# Connect and subscribe to AWS IoT
myMQTTClient.connect()
myMQTTClient.subscribe(topic, 1, customCallback)

while True:
    time.sleep(1)


