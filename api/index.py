from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

# 1. Initialize the App (Vercel looks for this specific variable 'app')
app = FastAPI()

# 2. Setup Google Gemini
# It grabs the key you saved in Vercel Environment Variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Define the data we expect from the frontend
class ImageRequest(BaseModel):
    image: str

# 4. The API Route
@app.post("/api")
async def analyze_skin(request: ImageRequest):
    try:
        # Select the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create the prompt for the AI
        prompt = "Analyze this skin in 3 short bullet points: 1) Skin Type guess, 2) Main concerns visible, 3) One recommended ingredient (like Salicylic Acid or Vitamin C). Keep it brief and friendly."

        # Prepare the image data (Gemini expects a specific format for raw bytes)
        # We wrap the base64 string into an image part
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': request.image},
            prompt
        ])
        
        # Return the text back to your phone
        return {"analysis": response.text}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": f"AI Analysis failed: {str(e)}"}
