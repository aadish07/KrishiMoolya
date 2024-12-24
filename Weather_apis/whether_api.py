from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your API key and base URL for WeatherAPI
API_KEY = "eae92d4850a64da4af7210109242312"  # Replace with your actual API key
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get state and district from the request (query parameters)
    state = request.args.get('state', '')  # Default empty string if not provided
    district = request.args.get('district', '')  # Default empty string if not provided

    # Combine state and district into a location string
    location = f"{district},{state}" if state and district else 'Delhi'  # Default to Delhi if empty inputs

    # Fetch weather data from WeatherAPI
    response = requests.get(
        BASE_URL,
        params={
            'key': API_KEY,
            'q': location,  # Location as district, state
            'days': 5        # Get 5 days forecast
        }
    )

    if response.status_code == 200:
        data = response.json()
        # Extract 5-day forecast with humidity
        forecast = [
            {
                'date': day['date'],
                'avg_temperature': day['day']['avgtemp_c'],  # Average temp in Celsius
                'condition': day['day']['condition']['text'],  # Weather condition (e.g., Sunny)
                'icon': day['day']['condition']['icon'],       # Icon URL for weather
                'humidity': day['day']['avghumidity'],         # Average humidity for the day
            }
            for day in data['forecast']['forecastday']
        ]
        
        # Extract current weather data for humidity
        current_weather = data['current']
        current_humidity = current_weather['humidity']  # Current air humidity

        return jsonify({
            'location': location,
            'forecast': forecast,
            'current_humidity': current_humidity  # Include current humidity data
        })
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3500)
