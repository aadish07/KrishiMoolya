from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load saved model, scaler, and label encoder if available
model_path = r"E:\Hackathon\agri-price-predictor\crop_recommendation\crop_recommendation\best_rf_model.joblib"
scaler_path = r"E:\Hackathon\agri-price-predictor\crop_recommendation\crop_recommendation\scaler.joblib"
encoder_path = r"E:\Hackathon\agri-price-predictor\crop_recommendation\crop_recommendation\label_encoder.joblib"

# Check if files exist
if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(encoder_path):
    print("Loading saved model, scaler, and encoder...")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
else:
    raise Exception("Saved model, scaler, or encoder files not found.")

@app.route('/croppredict', methods=['POST'])
def predict_crop():
    try:
        data = request.get_json()
        
        # Extract user inputs from the request
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        # Prepare input data and scale it
        user_input = [[N, P, K, temperature, humidity, ph, rainfall]]
        user_input_scaled = scaler.transform(user_input)

        # Predict the crop label
        predicted_label = label_encoder.inverse_transform(model.predict(user_input_scaled))

        return jsonify({
            'recommended_crop': predicted_label[0]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True,port=8080)
