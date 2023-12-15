import serial
import mysql.connector

# Configure the serial port
ser = serial.Serial('/dev/ttyS0', 9600)  # Arduino's serial port

#  MariaDB connection 
db_host = "localhost"
db_user = "root"
db_password = ""
db_name = "localdb"

 # Connect to MariaDB
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

cursor = db_connection.cursor()   

# Function to read motor state from the database
def get_motor_state():
    cursor.execute("SELECT value FROM motorState BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0

# Function to update motor state in the database
def update_motor_state(state):
    cursor.execute(f"INSERT INTO motorState (value) VALUES ({state})")
    db.commit()

# Read and write loop
while True:
    # Read motor state from the Arduino
    motor_state = get_motor_state()
    
    # Send motor state to Arduino
    ser.write(str(motor_state).encode())
    
    # Wait for a moment
    response = ser.readline().decode().strip()
    
    # Print Arduino's response
    print(response)
