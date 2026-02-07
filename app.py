from flask import Flask, render_template, request
import requests, sqlite3
from config import API_KEY, BASE_URL

app = Flask(__name__)

def save_to_db(city, temp, humidity, wind):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                        city TEXT, temp REAL, humidity INTEGER, wind REAL)''')
    cursor.execute("INSERT INTO weather_data VALUES (?, ?, ?, ?)", (city, temp, humidity, wind))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    if request.method == 'POST':
        city = request.form['city']
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            weather = {
                'city': city,
                'temp': response['main']['temp'],
                'humidity': response['main']['humidity'],
                'wind': response['wind']['speed']
            }
            save_to_db(city, weather['temp'], weather['humidity'], weather['wind'])
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)