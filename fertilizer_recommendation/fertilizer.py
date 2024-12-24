import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

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
file_path = "/Users/sanghvi/Downloads/SVCE/Recommendation/fertilizer_recommendation/fertilizer.csv"  # Replace with your file path
model_filename = "/Users/sanghvi/Downloads/SVCE/Recommendation/fertilizer_recommendation/fertilizer_model.pkl"

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
    with open("label_encoders.pkl", "wb") as le_file:
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
    with open("/Users/sanghvi/Downloads/SVCE/Recommendation/fertilizer_recommendation/label_encoders.pkl", "rb") as le_file:
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
    if nitrogen > 80:  # Example threshold
        suggestions.append(fertilizer_dic['NHigh'])
    elif nitrogen < 20:  # Example threshold
        suggestions.append(fertilizer_dic['Nlow'])
    
    if phosphorous > 60:  # Example threshold
        suggestions.append(fertilizer_dic['PHigh'])
    elif phosphorous < 20:  # Example threshold
        suggestions.append(fertilizer_dic['Plow'])
    
    if potassium > 60:  # Example threshold
        suggestions.append(fertilizer_dic['KHigh'])
    elif potassium < 20:  # Example threshold
        suggestions.append(fertilizer_dic['Klow'])
    
    return suggestions

# Get user input
print("\nEnter the input values for fertilizer recommendation:")
temperature = float(input("Temperature (°C): "))
humidity = float(input("Humidity (%): "))
moisture = float(input("Moisture (%): "))
soil_type = input("Soil Type (e.g., Loamy, Sandy, Clayey): ")
crop_type = input("Crop Type (e.g., Maize, Rice, Wheat): ")
nitrogen = int(input("Nitrogen (N) value: "))
potassium = int(input("Potassium (K) value: "))
phosphorous = int(input("Phosphorous (P) value: "))

# Predict and display the fertilizer recommendation
try:
    fertilizer_name = predict_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous)
    print(f"\nRecommended Fertilizer: {fertilizer_name}")
    
    # Display nutrient suggestions
    suggestions = get_nutrient_suggestions(nitrogen, potassium, phosphorous)
    print("\nNutrient Suggestions:")
    for suggestion in suggestions:
        print(suggestion)
except ValueError as e:
    print("\nError in input values. Please check and try again:", e)