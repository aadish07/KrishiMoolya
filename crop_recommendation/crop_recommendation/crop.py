import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib  # For saving and loading models
import os

# Load dataset
data = pd.read_csv("/Users/sanghvi/Downloads/SVCE/Recommendation/crop_recommendation/crop_recommendation.csv")

# Feature and target separation
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Check if a trained model already exists
model_path = "/Users/sanghvi/Downloads/SVCE/Recommendation/crop_recommendation/best_rf_model.joblib"
scaler_path = "/Users/sanghvi/Downloads/SVCE/Recommendation/crop_recommendation/scaler.joblib"
encoder_path = "/Users/sanghvi/Downloads/SVCE/Recommendation/crop_recommendation/label_encoder.joblib"

if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(encoder_path):
    print("Loading saved model, scaler, and encoder...")
    best_rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
else:
    print("Training the model...")

    # Random Forest with GridSearchCV for hyperparameter tuning
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }

    rf_model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, n_jobs=-1, scoring='accuracy', verbose=2)
    grid_search.fit(X_train_scaled, y_train)

    # Save the best model and other components
    best_rf_model = grid_search.best_estimator_
    joblib.dump(best_rf_model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(label_encoder, encoder_path)
    print("Model, scaler, and encoder saved!")

# Model evaluation
y_pred = best_rf_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nRandom Forest Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Take user input
print("Enter the values for prediction:")
N = float(input("N (Nitrogen content): "))
P = float(input("P (Phosphorus content): "))
K = float(input("K (Potassium content): "))
temperature = float(input("Temperature (°C): "))
humidity = float(input("Humidity (%): "))
ph = float(input("pH level: "))
rainfall = float(input("Rainfall (mm): "))

user_input = [[N, P, K, temperature, humidity, ph, rainfall]]
user_input_scaled = scaler.transform(user_input)

# Predict the crop
predicted_label = label_encoder.inverse_transform(best_rf_model.predict(user_input_scaled))
print(f"\nRecommended Crop: {predicted_label[0]}")