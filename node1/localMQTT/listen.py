# its subscribing

import paho.mqtt.client as mqtt
import mysql.connector

#  MariaDB connection 
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "localdb"

# Define the MQTT broker address and port
broker_address = "192.168.0.110"
broker_port = 1883

# Define the topics to subscribe to
topics = [  # my node is subscribing to all topics in our system, as our local side
# web server is on my node(mysha), so i have to have access to all data from everyone to update them
# as is on the web server hosted locally, which is a fail proof when theres no wifi
    "blindBack/data",
    "blindFront/data",
    "buzzer/data",
    "fanOn/data",
    "motorState/data",
    "patrolCar/data",
    "blindBackState/data",
    "blindFrontState/data",
]

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribe to the specified topics when connected
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    
    
# Function to update Maria
def update_database(topic, payload):
    try:
        # Connect to MariaDB
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Determine the table based on the topic
        table_name = topic.split("/")[1] + "Table"

        # Create the table if not exists
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                value VARCHAR(255)
            )
        ''')

        # Insert 
        cursor.execute(f"INSERT INTO {table_name} (value) VALUES (%s)", (payload,))

        # Commit  changes n close the connection
        connection.commit()
        connection.close()

        print(f"Updated {table_name} with value: {payload}")

    except mysql.connector.Error as e:
        print(f"Error updating database: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, 60)

# Loop to maintain the connection and handle incoming messages
client.loop_forever()
