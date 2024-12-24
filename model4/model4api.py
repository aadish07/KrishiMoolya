from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the models, scaler, and label encoders
min_price_model = joblib.load(r'E:\Hackathon\agri-price-predictor\model4\min_price_model.pkl')
max_price_model = joblib.load(r'E:\Hackathon\agri-price-predictor\model4\max_price_model.pkl')
scaler = joblib.load(r'E:\Hackathon\agri-price-predictor\model4\scaler.pkl')
label_encoders = pickle.load(open(r'E:\Hackathon\agri-price-predictor\model4\label_encoders.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        required_fields = ['date', 'crop', 'district']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get input data
        date = data['date']
        crop = data['crop']
        district = data['district']
        
        # Parse and preprocess date
        try:
            date = pd.to_datetime(date)
            date_ordinal = date.toordinal()
            year = date.year
            month = date.month
            day_of_year = date.dayofyear
        except Exception as e:
            return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
        
        # Encode crop and district
        try:
            crop_encoded = label_encoders['Crop'].transform([crop])[0]
            district_encoded = label_encoders['District'].transform([district])[0]
        except KeyError as e:
            return jsonify({'error': f'Invalid value for {str(e)}: Ensure that crop and district are valid'}), 400
        
        # Prepare input data with all necessary features
        input_data = np.array([[year, month, day_of_year, crop_encoded, district_encoded]])
        input_scaled = scaler.transform(input_data)  # Scale the input data
        
        # Predict min and max prices
        min_price = min_price_model.predict(input_scaled)[0]
        max_price = max_price_model.predict(input_scaled)[0]
        
        # Return predictions in the response
        return jsonify({
            'date': date.strftime('%Y-%m-%d'),
            'crop': crop,
            'district': district,
            'predicted_min_price': round(min_price, 2),
            'predicted_max_price': round(max_price, 2)
        })
    
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)