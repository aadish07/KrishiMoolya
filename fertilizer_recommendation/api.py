from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fertilizer recommendation dictionary
fertilizer_dic = {
    'NHigh': """The N value of soil is high and might give rise to weeds.
         Suggestions:
        1. Add manure
        2. Use coffee grounds
        3. Plant nitrogen-fixing plants
        4. Plant green manure crops like cabbage
        5. Use mulch""",
    
    'Nlow': """The N value of your soil is low.
         Suggestions:
        1. Add sawdust or woodchips
        2. Plant heavy nitrogen-feeding plants
        3. Add composted manure
        4. Use NPK fertilizers with high N value""",
    
    'PHigh': """The P value of your soil is high.
         Suggestions:
        1. Avoid adding manure
        2. Use phosphorus-free fertilizers
        3. Plant nitrogen-fixing vegetables""",
    
    'Plow': """The P value of your soil is low.
         Suggestions:
        1. Add bone meal or rock phosphate
        2. Use fertilizers with high P values
        3. Add organic compost""",
    
    'KHigh': """The K value of your soil is high.
         Suggestions:
        1. Loosen soil and water thoroughly
        2. Remove potassium-rich rocks
        3. Use fertilizers with low K values""",
    
    'Klow': """The K value of your soil is low.
         Suggestions:
        1. Add muricate or sulphate of potash
        2. Use potash fertilizers
        3. Bury banana peels below soil surface"""
}

# File paths
file_path = r"E:\Hackathon\agri-price-predictor\fertilizer_recommendation\fertilizer.csv"
model_filename = "fertilizer_model.pkl"  # Change the file path accordingly
label_encoders_filename = "label_encoders.pkl"

# Check if the model is already saved
if not os.path.exists(model_filename):
    print("Model not found. Training a new model...")

    # Load the dataset
    fertilizer_data = pd.read_csv(file_path)

    # Encode categorical columns
    label_encoders = {}
    for col in ['Soil Type', 'Crop Type', 'Fertilizer Name']:
        le = LabelEncoder()
        fertilizer_data[col] = le.fit_transform(fertilizer_data[col])
        label_encoders[col] = le

    # Save label encoders
    with open(label_encoders_filename, "wb") as le_file:
        pickle.dump(label_encoders, le_file)

    # Define features and target
    X = fertilizer_data.drop(columns=['Fertilizer Name'])
    y = fertilizer_data['Fertilizer Name']

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Random Forest model
    fertilizer_model = RandomForestClassifier(random_state=42)
    fertilizer_model.fit(X_train, y_train)

    # Save the trained model
    with open(model_filename, "wb") as model_file:
        pickle.dump(fertilizer_model, model_file)
    print("Model trained and saved successfully.")
else:
    print("Model found. Loading the saved model...")
    with open(label_encoders_filename, "rb") as le_file:
        label_encoders = pickle.load(le_file)

# Function to predict fertilizer recommendations
def predict_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous):
    # Encode categorical inputs
    soil_type_encoded = label_encoders['Soil Type'].transform([soil_type])[0]
    crop_type_encoded = label_encoders['Crop Type'].transform([crop_type])[0]
    
    # Prepare input data
    input_data = [[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorous]]
    
    # Load the trained model
    with open(model_filename, "rb") as model_file:
        model = pickle.load(model_file)
    
    # Predict fertilizer
    fertilizer_code = model.predict(input_data)[0]
    fertilizer_name = label_encoders['Fertilizer Name'].inverse_transform([fertilizer_code])[0]
    return fertilizer_name

# Function to get nutrient suggestions
def get_nutrient_suggestions(nitrogen, potassium, phosphorous):
    suggestions = []
    
    # Check nitrogen levels
    if nitrogen > 80:
        suggestions.append(fertilizer_dic['NHigh'])
    elif nitrogen < 30:
        suggestions.append(fertilizer_dic['Nlow'])
    
    # Check phosphorous levels
    if phosphorous > 70:
        suggestions.append(fertilizer_dic['PHigh'])
    elif phosphorous < 30:
        suggestions.append(fertilizer_dic['Plow'])
    
    # Check potassium levels
    if potassium > 70:
        suggestions.append(fertilizer_dic['KHigh'])
    elif potassium < 30:
        suggestions.append(fertilizer_dic['Klow'])
    
    # If no suggestions were added, provide a general suggestion based on average values
    if not suggestions:
        suggestions.append("The nutrient levels seem balanced. Keep monitoring and apply fertilizers accordingly.")

    return suggestions

@app.route('/fertilizerpredict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract inputs from the request
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        moisture = float(data['moisture'])
        soil_type = data['soil_type']
        crop_type = data['crop_type']
        nitrogen = int(data['nitrogen'])
        potassium = int(data['potassium'])
        phosphorous = int(data['phosphorous'])

        # Predict fertilizer recommendation
        fertilizer_name = predict_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous)
        
        # Get nutrient suggestions
        suggestions = get_nutrient_suggestions(nitrogen, potassium, phosphorous)

        return jsonify({
            'fertilizer_recommendation': fertilizer_name,
            'nutrient_suggestions': suggestions
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
