from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import pickle
from datetime import datetime
from flask_cors import CORS

# Load models, scaler, and label encoders
min_price_model = joblib.load(r'E:\Hackathon\agri-price-predictor\model34 (2)\model34\model3\min_price_model.pkl')
max_price_model = joblib.load(r'E:\Hackathon\agri-price-predictor\model34 (2)\model34\model3\max_price_model.pkl')
scaler = joblib.load(r'E:\Hackathon\agri-price-predictor\model34 (2)\model34\model3\scaler.pkl')
label_encoders = pickle.load(open(r'E:\Hackathon\agri-price-predictor\model34 (2)\model34\model3\label_encoders.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json
    
    # Validate input data
    required_fields = ['date', 'crop', 'district', 'temperature', 'rainfall', 'moisture']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Extract date components
        date = pd.to_datetime(data['date'])
        year = date.year
        month = date.month
        day_of_year = date.dayofyear
        
        # Encode categorical variables
        crop_encoded = label_encoders['Crop'].transform([data['crop']])[0]
        district_encoded = label_encoders['District'].transform([data['district']])[0]
        
        # Create input array with all features
        input_data = np.array([[
            year,              # Year
            month,             # Month
            day_of_year,       # Day of Year
            crop_encoded,      # Encoded Crop
            district_encoded,  # Encoded District
            data['temperature'],  # Temperature
            data['rainfall'],     # Rainfall
            data['moisture']      # Moisture
        ]])
        
        # Scale the input data
        input_scaled = scaler.transform(input_data)
        
        # Predict prices
        min_price = min_price_model.predict(input_scaled)[0]
        max_price = max_price_model.predict(input_scaled)[0]
        
        # Return predictions
        response = {
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2)
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
