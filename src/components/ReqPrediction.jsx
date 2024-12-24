import { useState } from "react";
import {
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
} from "@mui/material";
import axios from "axios";

const CropPredictionForm = () => {
  const [formData, setFormData] = useState({
    N: "",
    P: "",
    K: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Reset error
    setPrediction(null); // Reset prediction
    setLoading(true); // Show loading state

    try {
      // Make POST request to the Flask API
      const response = await axios.post(
        "http://127.0.0.1:8080/croppredict",
        formData
      );
      setPrediction(response.data.recommended_crop); // Display prediction result
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to fetch prediction. Please try again."
      );
      console.error(err);
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Box
      sx={{
        maxWidth: "100vw",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg, #f5f7fa, #c3cfe2)",
        padding: 2,
      }}
    >
      <Card sx={{ width: "90%", maxWidth: 700 }}>
        <CardContent>
          <Typography
            variant="h5"
            component="div"
            gutterBottom
            sx={{ textAlign: "center", mb: 2 }}
          >
            Crop Recommendation
          </Typography>

          <form onSubmit={handleSubmit}>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                gap: 2,
              }}
            >
              {/* Input Fields */}
              {[
                { name: "N", label: "Nitrogen (N)" },
                { name: "P", label: "Phosphorous (P)" },
                { name: "K", label: "Potassium (K)" },
                { name: "temperature", label: "Temperature (°C)" },
                { name: "humidity", label: "Humidity (%)" },
                { name: "ph", label: "pH Level" },
                { name: "rainfall", label: "Rainfall (mm)" },
              ].map((field) => (
                <TextField
                  key={field.name}
                  name={field.name}
                  label={field.label}
                  type="number"
                  value={formData[field.name]}
                  onChange={handleChange}
                  variant="outlined"
                  fullWidth
                />
              ))}

              {/* Submit Button */}
              <Button
                variant="contained"
                color="success"
                type="submit"
                fullWidth
                sx={{ mt: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : "Recommend Crop"}
              </Button>
            </Box>
          </form>

          {/* Result Section */}
          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
          {prediction && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" sx={{ textAlign: "center" }}>
                Recommended Crop:{" "}
                <Typography component="strong">{prediction}</Typography>
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default CropPredictionForm;
