# KrishiMoolya
AIML based Crop Price Prediction Model

### KrishiMoolya 🌾  
Welcome to **Krishi Moolya** – A platform that leverages technology to predict crop prices, empowering farmers with actionable insights for a better tomorrow.  

---

## 🚀 Project Overview  
KrishiMoolya is a crop price prediction tool designed to assist farmers, traders, and decision-makers in planning their agriculture-related activities. By utilizing historical data and advanced algorithms, this platform provides accurate price forecasts for various crops.  

---

## 🛠 Features  
- **State and District Selection:** Choose your region to get localized predictions.  
- **Crop Selection:** Select from a list of popular crops to predict prices.  
- **Date-based Forecasts:** Get price predictions up to 3 months in the future.  
- **Real-time Results:** View minimum and maximum price ranges for better decision-making.  
- **Error Alerts:** Clear and concise error messages for any issues during prediction.
- **Offline Chatbots
- **Online Gemini Chatbot
- **Crop and Fertilizer Recommendation
- **Price Prediction considering all necessary factors with more than 96% Accuracy
- **Weather Prediction of next 5 days
- **Interactive Dashboard

---

## 📦 Tech Stack  
### Frontend  
- **React**: For building an intuitive user interface.  
- **Material-UI**: For sleek, responsive components and styling.  

### Backend  
- **Flask**: Serves the prediction API and handles business logic.  
- **Python**: Utilized for data processing and machine learning models.  

### Deployment  
- **Localhost (Development)**: Hosted locally for testing and development purposes.  

---

## 🖥️ Installation Guide  
Follow these steps to set up the project on your local machine.  

### Prerequisites  
Ensure you have the following installed:  
- Node.js and npm  
- Python 3.2 and above 
- Flask  
- Required Python libraries (`flask`, `pandas`, etc.)  

### Steps  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/KrishiMoolya.git  
   ```  

2. Navigate to the frontend directory and install dependencies:  
   ```bash  
   cd frontend  
   npm install  
   ```  

3. Start the frontend:  
   ```bash  
   npm start  
   ```  

4. Navigate to the backend directory and set up Python environment:  
   ```bash  
   cd backend  
   pip install -r requirements.txt  
   ```  

5. Run the Flask server:  
   ```bash  
   python app.py  
   ```  

6. Open your browser and access the app at:  
   ```  
   http://localhost:3000  
   ```  

---

## 🧩 API Endpoints  

### 1. **POST `/predict`**  
Predicts crop prices based on input parameters.  

#### Request Body  
```json  
{  
  "state": "Madhya Pradesh",  
  "district": "Indore",  
  "crop": "Wheat",  
  "date": "2024-12-31"  
}  
```  

#### Response  
```json  
{  
  "predicted_min_price": 2500,  
  "predicted_max_price": 2700  
}  
```  

#### Error Response  
```json  
{  
  "error": "Invalid input or server issue"  
}  
```  

---

## 🎯 How It Works  
1. The user selects the **state**, **district**, **crop**, and **date** through an interactive form.  
2. The frontend sends the data to the Flask backend via a POST request.  
3. The backend processes the input and queries a trained model to predict price ranges.  
4. The frontend displays the predicted minimum and maximum prices to the user.  

---

## 🌟 Contributing  
We welcome contributions to improve **KrishiMoolya**!  

1. Fork the repository.  
2. Create a new branch for your feature:  
   ```bash  
   git checkout -b feature-name  
   ```  
3. Commit your changes:  
   ```bash  
   git commit -m "Add feature description"  
   ```  
4. Push your branch:  
   ```bash  
   git push origin feature-name  
   ```  
5. Open a Pull Request and explain your changes.  

---

## 📜 License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## 📬 Contact  
Have questions or suggestions? Feel free to reach out!  
- **Email:** radharamangurjar4104@gmail.com  
- **GitHub:** [Radharamangurjar315](https://github.com/Radharamangurjar315)  

Let’s build a brighter future for agriculture together! 🌱  
