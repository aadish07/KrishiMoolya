from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Set your Google Gemini API Key (replace with your actual API key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAHRwVNpM9r3E3XBBr14nPSy6r8OnLqe5g")  # Store this securely

# Validate the API key
if GEMINI_API_KEY == "your_gemini_api_key":
    raise ValueError("Replace 'your_gemini_api_key' with your actual API key.")

# Define the input data model
class InputData(BaseModel):
    crop: str
    land_area: float  # in acres
    soil_quality: str
    season: str

@app.post("/recommendations/")
async def get_recommendations(data: InputData):
    """
    Fetch detailed recommendations for agricultural practices based on user input.
    """
    # Construct the prompt for the model
    prompt = f"""
    My crop type is {data.crop}, my land area in acres is {data.land_area}, my land soil type is {data.soil_quality}, and the season is {data.season}.
    Provide detailed recommendations for the following:
    1. {data.crop} seed variety in quintals.
    2. Fertilizers (NPK) required in quintals.
    3. Time required to grow {data.crop} in months.
    4. Water required in liters.
    Also, suggest tools required based on the crop type, land area, soil quality, and season.
    """

    # Google Gemini API endpoint (Update with the correct endpoint if necessary)
    gemini_url ="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}" 


    # Payload for the Gemini API request
    payload = {
        "model": "gemini-large",  # Use the correct model name
        "prompt": prompt,
        "max_tokens": 1000,  # Increase for more comprehensive responses
        "temperature": 0.7
    }

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Send the request to the Gemini API
        response = requests.post(gemini_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Parse the JSON response
        result = response.json()
        if "choices" not in result or not result["choices"]:
            raise HTTPException(status_code=500, detail="No valid response from the model.")

        # Extract the model's response text
        recommendations = result["choices"][0]["text"].strip()

        # Optional: Organize the response for frontend rendering
        structured_response = {
            "crop": data.crop,
            "land_area": f"{data.land_area} acres",
            "soil_quality": data.soil_quality,
            "season": data.season,
            "recommendations": recommendations
        }

        return structured_response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch recommendations: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")