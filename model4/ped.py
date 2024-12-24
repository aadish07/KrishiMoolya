import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import joblib

# # Load the dataset (used for training and label encoding purposes)
# data = pd.read_csv('/Users/sanghvi/Downloads/SVCE/data/final.csv')

# # Encode categorical columns
# label_encoders = {}
# for col in ['Crop', 'District']:
#     le = LabelEncoder()
#     data[col] = le.fit_transform(data[col])
#     label_encoders[col] = le

# # Extract Date components
# data['Year'] = data['Date'].apply(lambda x: pd.to_datetime(x).year)
# data['Month'] = data['Date'].apply(lambda x: pd.to_datetime(x).month)
# data['DayOfYear'] = data['Date'].apply(lambda x: pd.to_datetime(x).dayofyear)

# # Define features and target
# X = data[['Year', 'Month', 'DayOfYear', 'Crop', 'District']]
# y_min = data['Min_Price']
# y_max = data['Max_Price']

# # Split the data for training
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_min_train, y_min_test, y_max_train, y_max_test = train_test_split(
#     X, y_min, y_max, test_size=0.2, random_state=42
# )

# # Scale the features
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# # Train the Random Forest model
# min_price_model = RandomForestRegressor()
# max_price_model = RandomForestRegressor()

# min_price_model.fit(X_train, y_min_train)
# max_price_model.fit(X_train, y_max_train)

# # Save the models and scaler for later use
# joblib.dump(min_price_model, 'min_price_model.pkl')
# joblib.dump(max_price_model, 'max_price_model.pkl')
# joblib.dump(scaler, 'scaler.pkl')
# pickle.dump(label_encoders, open('label_encoders.pkl', 'wb'))

print("Models and encoders saved successfully!")

# Load the models and scaler
min_price_model = joblib.load('/Users/sanghvi/Downloads/SVCE/model4/min_price_model.pkl')
max_price_model = joblib.load('/Users/sanghvi/Downloads/SVCE/model4/max_price_model.pkl')
scaler = joblib.load('/Users/sanghvi/Downloads/SVCE/model4/scaler.pkl')
label_encoders = pickle.load(open('/Users/sanghvi/Downloads/SVCE/model4/label_encoders.pkl', 'rb'))

# Function to take user input and predict prices
def predict_prices():
    # Get user inputs
    date = input("Enter the date (YYYY-MM-DD): ")
    crop = input("Enter the crop: ")
    district = input("Enter the district: ")
    
    # Preprocess inputs
    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    day_of_year = date.dayofyear
    crop_encoded = label_encoders['Crop'].transform([crop])[0]
    district_encoded = label_encoders['District'].transform([district])[0]
    
    # Create input array
    input_data = np.array([[year, month, day_of_year, crop_encoded, district_encoded]])
    input_scaled = scaler.transform(input_data)
    
    # Predict prices
    min_price = min_price_model.predict(input_scaled)[0]
    max_price = max_price_model.predict(input_scaled)[0]
    
    print(f"Predicted Min Price: {min_price:.2f}")
    print(f"Predicted Max Price: {max_price:.2f}")

# Run the prediction function
predict_prices()
