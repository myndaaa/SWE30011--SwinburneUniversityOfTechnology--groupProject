
import time
import json
import mysql.connector
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.publish as publish

# Local DB connection
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="localdb")

# AWS IoT certificate based connection

myMQTTClient.configureEndpoint("a3n3c0xu4k20cn-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert/AmazonRootCA1.pem", "/home/pi/cert/cb53821e62b7edc905dc7d37abe4d1df422e9e5589666d87c151d683b7c2355d-private.pem", "/home/pi/cert/cb53821e62b7edc905dc7d37abe4d1df422e9e5589666d87c151d683b7c2355d-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

topic = "node1_publish"
# Connect and publish
myMQTTClient.connect()

while True:
    with mydb.cursor() as mycursor:
        # Query the latest values from each table
        mycursor.execute("SELECT value FROM dht11 ORDER BY id DESC LIMIT 1")
        dht11_value = mycursor.fetchone()[0]

        mycursor.execute("SELECT value FROM rain ORDER BY id DESC LIMIT 1")
        rain_value = mycursor.fetchone()[0]

        mycursor.execute("SELECT value FROM soil ORDER BY id DESC LIMIT 1")
        soil_value = mycursor.fetchone()[0]

        mycursor.execute("SELECT value FROM smoke ORDER BY id DESC LIMIT 1")
        smoke_value = mycursor.fetchone()[0]

    # Create a dictionary with the sensor values
    sensor_data = {
        "dht11": float(dht11_value),
        "rain": float(rain_value),
        "soil": float(soil_value),
        "smoke": float(smoke_value)
    }

    # Convert dictionary to JSON
    json_data = json.dumps(sensor_data)

    # Publish data to the specified topic
    myMQTTClient.publish(topic, json_data, 0)

    print("Data published to", topic, ":", json_data)

    time.sleep(120)  # Delay of 2 minutes


