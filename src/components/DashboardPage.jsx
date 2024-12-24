import { useState, useEffect } from "react";
import axios from "axios";  // Import axios for making requests
import "./DashboardPage.css";  // Import the CSS file

const WeatherDashboard = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const response = await axios.get('http://localhost:3500/weather');
        setWeatherData(response.data);
      } catch (err) {
        setError("Error fetching weather data", err);
      }
    };

    fetchWeatherData();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!weatherData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="weather-dashboard">
      <h1>Weather in {weatherData.location}</h1>
      <p>Current Humidity: {weatherData.current_humidity}%</p>

      <div className="forecast-container">
        {weatherData.forecast.map((day, index) => (
          <div key={index} className="forecast-box">
            <h3>{day.date}</h3>
            <p><strong>Avg Temp:</strong> {day.avg_temperature}°C</p>
            <p><strong>Condition:</strong> {day.condition}</p>
            <p><strong>Humidity:</strong> {day.humidity}%</p>
            <img src={`https:${day.icon}`} alt={day.condition} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default WeatherDashboard;
