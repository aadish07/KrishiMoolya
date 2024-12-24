import { useState } from 'react';
import "./PredictionPage.css";
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  MenuItem,
  FormControl,
  Select,
  InputLabel,
  Alert,
  CircularProgress
} from '@mui/material';

const PricePredictionForm = () => {
  const [formData, setFormData] = useState({
    state: '',
    district: '',
    crop: '',
    date: '',
    temperature: '',
    rainfall: '',
    moisture: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Define your state districts
  const districts = {
    "Madhya Pradesh": [
      "Betul", "Bhopal", "Chhindwara", "Dewas", "Gwalior", "Indore", "Jabalpur",
      "Khargone", "Ratlam", "Rewa", "Sagar", "Satna", "Shivpuri", "Ujjain", "Vidisha"
    ]
  };

  // Define your commodities
  const crops = [
    'Wheat', 'Gram', 'Barley', 'Rice', 'Maize', 'Jowar', 'Soybean', 'Masoor', 'Groundnuts'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Log the request data
      console.log('Sending request with data:', {
        date: formData.date,
        crop: formData.crop,
        district: formData.district,
        temperature: formData.temperature,
        rainfall: formData.rainfall,
        moisture: formData.moisture,
      });

      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        credentials: 'omit',
        body: JSON.stringify({
          date: formData.date,
          crop: formData.crop,
          district: formData.district,
          temperature: formData.temperature,
          rainfall: formData.rainfall,
          moisture: formData.moisture
        }),
      });

      console.log('Response status:', response.status);
      
      // Read the response as JSON
      let data;
      try {
        // Check if the response is okay before parsing
        if (!response.ok) {
          const responseText = await response.text(); // Read the response text if not ok
          console.log('Error response text:', responseText);
          throw new Error(`Failed to get prediction: ${responseText}`);
        }

        // Parse the response as JSON only if the response is ok
        data = await response.json();
        console.log('Parsed response data:', data);

      } catch (err) {
        console.error('Error parsing response:', err);
        throw new Error('Invalid response format or server error');
      }
      setPrediction(data);
    } catch (err) {
      console.error('Error in handleSubmit:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
      ...(name === 'state' ? { districts: '' } : {}), // Reset district when state changes
    }));
  };
  

  // Get today's date for max date restriction
  const today = new Date().toISOString().split('T')[0];
  // Get date 3 months from today for max future prediction
  const maxDate = new Date();
  maxDate.setMonth(maxDate.getMonth() + 3);
  const maxDateString = maxDate.toISOString().split('T')[0];

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3}>
        <Box 
          sx={{ 
            bgcolor: 'success.main', 
            color: 'primary.contrastText',
            p: 3,
            textAlign: 'center',
            borderRadius: '4px 4px 0 0'
          }}
        >
          <Typography variant="h4" component="h1" style={{ color: 'white', fontFamily: 'cursive' }}>
            Price Prediction
          </Typography>
        </Box>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {/* State Selection */}
            <FormControl fullWidth required>
              <InputLabel>Select State</InputLabel>
              <Select
                name="state"
                value={formData.state}
                label="Select State"
                onChange={handleChange}
              >
                {Object.keys(districts).sort().map((state) => (
                  <MenuItem key={state} value={state}>
                    {state}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* District Selection */}
            <FormControl fullWidth required disabled={!formData.state}>
              <InputLabel>Select District</InputLabel>
              <Select
                name="district"
                value={formData.district}
                label="Select District"
                onChange={handleChange}
              >
                {formData.state && districts[formData.state].sort().map((district) => (
                  <MenuItem key={district} value={district}>
                    {district}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            {/* Commodity Selection */}
            <FormControl fullWidth required>
              <InputLabel>Select Commodity</InputLabel>
              <Select
                name="crop"
                value={formData.crop}
                label="Select Commodity"
                onChange={handleChange}
              >
                {crops.sort().map((crop) => (
                  <MenuItem 
                    key={crop} 
                    value={crop}
                  >
                    {crop}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Date Selection */}
            <TextField
              fullWidth
              required
              type="date"
              name="date"
              label="Select Date"
              value={formData.date}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              inputProps={{
                min: today,
                max: maxDateString
              }}
            />

            {/* Temperature Input */}
            <TextField
              fullWidth
              required
              type="number"
              name="temperature"
              label="Temperature (°C)"
              value={formData.temperature}
              onChange={handleChange}
            />

            {/* Rainfall Input */}
            <TextField
              fullWidth
              required
              type="number"
              name="rainfall"
              label="Rainfall (mm)"
              value={formData.rainfall}
              onChange={handleChange}
            />

            {/* Moisture Input */}
            <TextField
              fullWidth
              required
              type="number"
              name="moisture"
              label="Moisture (%)"
              value={formData.moisture}
              onChange={handleChange}
            />

            <Button 
              type="submit" 
              variant="contained" 
              size="large"
              sx={{ 
                mt: 2,
                bgcolor: 'success.main',
                '&:hover': {
                  bgcolor: 'success.dark',
                },
                height: '48px'
              }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Predict Price'}
            </Button>
          </Box>
        </Box>

        {/* Error Display */}
        {error && (
          <Box sx={{ p: 3 }}>
            <Alert 
              severity="error"
              onClose={() => setError(null)}
              sx={{ '& .MuiAlert-message': { width: '100%' } }}
            >
              {error}
            </Alert>
          </Box>
        )}

        {/* Prediction Results */}
        {prediction && (
          <Box sx={{ p: 3, borderTop: 1, borderColor: 'divider' }}>
            <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
              Predicted Price Range
            </Typography>
            <Box sx={{ 
              display: 'flex', 
              gap: 4, 
              flexWrap: 'wrap',
              bgcolor: 'background.paper',
              p: 2,
              borderRadius: 1
            }}>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Minimum Price
                </Typography>
                <Typography variant="h5" color="success.main">
                  ₹{prediction.min_price}
                  
                </Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Maximum Price
                </Typography>
                <Typography variant="h5" color="success.main">
                  ₹{prediction.max_price}
                </Typography>
              </Box>
            </Box>
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default PricePredictionForm;
