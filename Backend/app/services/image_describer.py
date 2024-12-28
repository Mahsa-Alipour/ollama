import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")  
LLM_API_PORT = os.getenv("LLM_API_PORT")  
MODEL_NAME = os.getenv("MODEL_NAME")  

FULL_API_URL = f"{LLM_API_URL}:{LLM_API_PORT}/api/generate"

def generate_response_with_image(prompt: str, image_data: bytes) -> dict:
    """
    Sends a prompt and image data to the LLM API and returns the JSON response.
    """
    try:
        response = requests.post(
            FULL_API_URL,  
            json={
                "prompt": prompt,
                "stream": False,
                "model": MODEL_NAME,  
                "image": image_data.hex()  
            }
        )

        if response.status_code == 200:
            return response.json() 
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get response from LLM: {response.text}"
            )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while contacting LLM: {str(e)}")
