import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import joblib

# Load the dataset (used for training and label encoding purposes)
data = pd.read_csv('/Users/sanghvi/Downloads/SVCE/data/final.csv')
 
# Encode categorical columns
label_encoders = {}
for col in ['Crop', 'District']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Convert Date to numerical format
data['Date'] = pd.to_datetime(data['Date']).map(pd.Timestamp.toordinal)

# Extract Date components
data['Year'] = data['Date'].apply(lambda x: pd.to_datetime(x).year)
data['Month'] = data['Date'].apply(lambda x: pd.to_datetime(x).month)
data['DayOfYear'] = data['Date'].apply(lambda x: pd.to_datetime(x).dayofyear)

# Define features and target
X = data[['Year', 'Month', 'DayOfYear', 'Crop', 'District', 'Temperature (°C)', 'Rainfall (mm)', 'Moisture (%)']]
y_min = data['Min_Price']
y_max = data['Max_Price']

# Split the data for training
from sklearn.model_selection import train_test_split
X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test = train_test_split(
    X, y_min, y_max, test_size=0.2, random_state=42
)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the Random Forest model
min_price_model = RandomForestRegressor(random_state=42)
max_price_model = RandomForestRegressor(random_state=42)

min_price_model.fit(X_train, y_min_train)
max_price_model.fit(X_train, y_max_train)

# Evaluate models using error metrics
# Minimum price model
y_min_pred = min_price_model.predict(X_test)
min_r2 = r2_score(y_min_test, y_min_pred)
min_rmse = np.sqrt(mean_squared_error(y_min_test, y_min_pred))
min_mae = mean_absolute_error(y_min_test, y_min_pred)
min_mse = mean_squared_error(y_min_test, y_min_pred)

print("Minimum Price Model Metrics:")
print(f"R² Score: {min_r2:.4f}")
print(f"RMSE: {min_rmse:.4f}")
print(f"MAE: {min_mae:.4f}")
print(f"MSE: {min_mse:.4f}")

# Maximum price model
y_max_pred = max_price_model.predict(X_test)
max_r2 = r2_score(y_max_test, y_max_pred)
max_rmse = np.sqrt(mean_squared_error(y_max_test, y_max_pred))
max_mae = mean_absolute_error(y_max_test, y_max_pred)
max_mse = mean_squared_error(y_max_test, y_max_pred)

print("\nMaximum Price Model Metrics:")
print(f"R² Score: {max_r2:.4f}")
print(f"RMSE: {max_rmse:.4f}")
print(f"MAE: {max_mae:.4f}")
print(f"MSE: {max_mse:.4f}")

# Save the models and scaler for later use
# joblib.dump(min_price_model, 'min_price_model.pkl')
# joblib.dump(max_price_model, 'max_price_model.pkl')
# joblib.dump(scaler, 'scaler.pkl')
# pickle.dump(label_encoders, open('label_encoders.pkl', 'wb'))

# Function to take user input and predict prices
def predict_prices():
    # Get user inputs
    date = input("Enter the date (YYYY-MM-DD): ")
    crop = input("Enter the crop: ")
    district = input("Enter the district: ")
    
    # Preprocess inputs
    date_ordinal = pd.to_datetime(date).toordinal()
    crop_encoded = label_encoders['Crop'].transform([crop])[0]
    district_encoded = label_encoders['District'].transform([district])[0]
    
    # Create input array
    input_data = np.array([[date_ordinal, crop_encoded, district_encoded]])
    input_scaled = scaler.transform(input_data)
    
    # Predict prices
    min_price = min_price_model.predict(input_scaled)[0]
    max_price = max_price_model.predict(input_scaled)[0]
    
    print(f"Predicted Min Price: {min_price:.2f}")
    print(f"Predicted Max Price: {max_price:.2f}")

# Run the prediction function
predict_prices()

# Minimum Price Model Metrics:
# R² Score (0.9992): Excellent fit; the model explains 99.92% of the variability in the minimum price data.
# RMSE (50.5269): Indicates the average error in the same units as the target variable. A lower value is good, and this is quite low relative to typical agricultural price ranges.
# MAE (10.4395): Very low absolute error, suggesting the predictions are close to the actual values.
# MSE (2552.9725): Also low, aligning with the good RMSE.
# Conclusion: This model is highly accurate and suitable for predicting the minimum price.

# Maximum Price Model Metrics:
# R² Score (0.9942): Still an excellent fit, explaining 99.42% of the variability in the maximum price data.
# RMSE (151.0701): The average error is higher than the minimum price model, which could indicate that maximum prices are harder to predict accurately.
# MAE (115.1492): Higher absolute error than the minimum price model, reflecting a potential need for further tuning.
# MSE (22822.1678): High compared to the minimum price model, but this aligns with the higher RMSE.
# Conclusion: While still very accurate, the maximum price model could benefit from additional optimization, such as hyperparameter tuning, feature engineering, or using an ensemble of models.