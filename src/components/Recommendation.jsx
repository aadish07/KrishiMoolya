import { useState } from "react";
import {
  Card,
  CardContent,
  TextField,
  Button,
  MenuItem,
  Typography,
  Box,
  Alert,
} from "@mui/material";

const FertilizerForm = () => {
  const [formData, setFormData] = useState({
    temperature: "",
    humidity: "",
    moisture: "",
    soilType: "",
    cropType: "",
    nitrogen: "",
    phosphorous: "",
    potassium: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/fertilizerpredict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          temperature: formData.temperature,
          humidity: formData.humidity,
          moisture: formData.moisture,
          soil_type: formData.soilType,
          crop_type: formData.cropType,
          nitrogen: formData.nitrogen,
          phosphorous: formData.phosphorous,
          potassium: formData.potassium,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data from the server.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
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
            Fertilizer Recommendation
          </Typography>

          <form onSubmit={handleSubmit}>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                gap: 2,
              }}
            >
              <TextField
                label="Temperature (°C)"
                name="temperature"
                type="number"
                value={formData.temperature}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />

              <TextField
                label="Humidity (%)"
                name="humidity"
                type="number"
                value={formData.humidity}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />

              <TextField
                label="Moisture (%)"
                name="moisture"
                type="number"
                value={formData.moisture}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />

              <TextField
                select
                label="Soil Type"
                name="soilType"
                value={formData.soilType}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              >
                <MenuItem value="Red">Red</MenuItem>
                <MenuItem value="Loamy">Loamy</MenuItem>
                <MenuItem value="Sandy">Sandy</MenuItem>
                <MenuItem value="Clayey">Clayey</MenuItem>
              </TextField>

              <TextField
                select
                label="Crop Type"
                name="cropType"
                value={formData.cropType}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              >
                <MenuItem value="Soyabean">Soyabean</MenuItem>
                <MenuItem value="Maize">Maize</MenuItem>
                <MenuItem value="Rice">Rice</MenuItem>
                <MenuItem value="Wheat">Wheat</MenuItem>
              </TextField>

              <TextField
                label="Nitrogen (N)"
                name="nitrogen"
                type="number"
                value={formData.nitrogen}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />

              <TextField
                label="Phosphorous (P)"
                name="phosphorous"
                type="number"
                value={formData.phosphorous}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />

              <TextField
                label="Potassium (K)"
                name="potassium"
                type="number"
                value={formData.potassium}
                onChange={handleInputChange}
                variant="outlined"
                fullWidth
              />
            </Box>

            <Button
              variant="contained"
              color="primary"
              type="submit"
              fullWidth
              sx={{ mt: 2 }}
              disabled={loading}
            >
              {loading ? "Submitting..." : "Recommend Ferilizer"}
            </Button>
          </form>

          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
          {result && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6">Recommended Fertilizer</Typography>
              <Typography>{result.fertilizer_recommendation}</Typography>

              <Typography variant="h6" sx={{ mt: 2 }}>
                Nutrient Suggestions:
              </Typography>
              <ul>
                {result.nutrient_suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default FertilizerForm;
