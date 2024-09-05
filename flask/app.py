from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configure connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",  
    database="localdb"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('login.html', error='Please enter both username and password')

    # Check credentials against the database
    cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        # Successful login
        return redirect(url_for('index'))
    else:
        # Failed login
        return render_template('login.html', error='Invalid credentials')


@app.route('/signup', methods=['POST'])
def handle_signup():
    signup_username = request.form.get('signup_username')
    signup_email = request.form.get('signup_email')
    signup_password = request.form.get('signup_password')

    if not signup_username or not signup_email or not signup_password:
        return render_template('login.html', signup_error='Please fill in all fields for signup')

    # Check if the username is already taken (adjust the query accordingly)
    cursor.execute("SELECT * FROM login WHERE username = %s", (signup_username,))
    if cursor.fetchone():
        return render_template('login.html', signup_error='Username already exists, please choose another')

    # Hash the password before storing it
    hashed_password = generate_password_hash(signup_password, method='sha256')

    # Insert the new user into the database
    cursor.execute("INSERT INTO login (username, email, password) VALUES (%s, %s, %s)", (signup_username, signup_email, hashed_password))
    db.commit()

    # Redirect to index or login page
    return redirect(url_for('index'))


        
@app.route('/index')
def index():
    return render_template('index.html') #nothing deployed from db so just rende static

@app.route('/about')
def about(): #nothing form db, only rendered from static
    return render_template('about.html')

@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        # Handle form submission
        motor_state = request.form.get('motorToggle')
        front_blind_state = request.form.get('frontBlindSlider')
        back_blind_state = request.form.get('backBlindSlider')
        buzzer_state = request.form.get('buzzerButton')
        patrol_state = request.form.get('patrolToggle')

        # Insert data into the respective tables
        cursor.execute("INSERT INTO motorState (state) VALUES (%s)", (motor_state,))
        cursor.execute("INSERT INTO fanFrontState (state) VALUES (%s)", (front_blind_state,))
        cursor.execute("INSERT INTO fanBackState (state) VALUES (%s)", (back_blind_state,))
        cursor.execute("INSERT INTO buzzerState (state) VALUES (%s)", (buzzer_state,))
        cursor.execute("INSERT INTO patrolState (state) VALUES (%s)", (patrol_state,))

        db.commit()

    return render_template('product.html')


@app.route('/enquire')
def enquire():
    return render_template('enquire.html') # video streaming is done via webcam.js on static

def generate_plot_image(data, ylabel, title):
    plt.figure(figsize=(8, 6))
    plt.plot(data['dates'], data['values'])
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.title(title)
    
    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

@app.route('/enhancements')
def enhancements():
    
    cursor.execute("SELECT date, value FROM rain WHERE date >= CURDATE() - INTERVAL 7 DAY")
    rain_data = cursor.fetchall()

   
    cursor.execute("SELECT date, value FROM soilMoisture WHERE date >= CURDATE() - INTERVAL 7 DAY")
    soil_moisture_data = cursor.fetchall()

    # Process the data to prepare for plotting
    rain_dates = [str(entry[0]) for entry in rain_data]
    rain_values = [entry[1] for entry in rain_data]

    soil_moisture_dates = [str(entry[0]) for entry in soil_moisture_data]
    soil_moisture_values = [entry[1] for entry in soil_moisture_data]

    # Create plots
    rain_plot = generate_plot_image({'dates': rain_dates, 'values': rain_values}, 'Rain (0-1)', 'Raining Graph')
    moisture_plot = generate_plot_image({'dates': soil_moisture_dates, 'values': soil_moisture_values}, 'Soil Moisture (%)', 'Soil Moisture Graph')

    
    # Fetch the latest data for rain, soil moisture, inside temperature, and outside temperature
    cursor.execute("SELECT value FROM rain ORDER BY date DESC LIMIT 1")
    latest_rain = cursor.fetchone()[0] if cursor.rowcount else 'N/A'

    cursor.execute("SELECT value FROM soilMoisture ORDER BY date DESC LIMIT 1")
    latest_soil_moisture = cursor.fetchone()[0] if cursor.rowcount else 'N/A'

    cursor.execute("SELECT value FROM tempIn ORDER BY date DESC LIMIT 1")
    latest_inside_temp = cursor.fetchone()[0] if cursor.rowcount else 'N/A'

    cursor.execute("SELECT value FROM tempOut ORDER BY date DESC LIMIT 1")
    latest_outside_temp = cursor.fetchone()[0] if cursor.rowcount else 'N/A'

    return render_template('enhancements.html', 
                           latest_rain=latest_rain,
                           
                           latest_soil_moisture=latest_soil_moisture,
                           latest_inside_temp=latest_inside_temp,
                           latest_outside_temp=latest_outside_temp,
                           rain_plot=rain_plot, moisture_plot=moisture_plot)

@app.route('/login') # if prssed on logout button, 
def login():
    return render_template('login.html')  
    
    
if __name__ == '__main__':
    app.run(debug=True)
