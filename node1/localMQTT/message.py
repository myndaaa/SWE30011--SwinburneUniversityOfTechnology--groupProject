
import mysql.connector
import paho.mqtt.client as mqtt

#MQTT broker address and port
broker_address = "192.168.0.102"
broker_port = 1883


#  MariaDB connection 
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "localdb"


#topic to publish to
publish_topic = "exhaustOn/data"

# Callback when a new record is inserted into the smoke table
def on_new_record(record):
    # Publish the record to the "exhaustOn" topic
    client.publish(publish_topic, str(record))

# Function to monitor changes in the database
def monitor_database_changes():
    try:
        # Connect to Maria
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Start monitoring changes in the smoke table
        cursor.execute("SELECT * FROM smoke ORDER BY id DESC LIMIT 1")
        last_record = cursor.fetchone()

        while True:
            cursor.execute("SELECT * FROM smoke ORDER BY id DESC LIMIT 1")
            new_record = cursor.fetchone()

            if new_record != last_record:
                on_new_record(new_record)
                last_record = new_record

    except mysql.connector.Error as e:
        print(f"Error monitoring database changes: {e}")

    finally:
        if connection.is_connected():
            connection.close()

# MQTT client setup
client = mqtt.Client()
client.connect(broker_address, broker_port, 60)

# Start monitoring changes in the database in a separate thread
monitor_database_changes()
