import serial
import MySQLdb

# Configure the serial port
ser = serial.Serial('COM3', 9600)  # Arduino's serial port

# Connect to the MySQL database
db = MySQLdb.connect(host="localhost", user="root", password="", db="localdb")
cursor = db.cursor()

# Function to read motor state from the database
def get_motor_state():
    cursor.execute("SELECT motorState FROM your_table_name ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0

# Function to update motor state in the database
def update_motor_state(state):
    cursor.execute(f"INSERT INTO your_table_name (motorState) VALUES ({state})")
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
