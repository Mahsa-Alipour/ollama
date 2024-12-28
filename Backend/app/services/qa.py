import os
from dotenv import load_dotenv
import requests
from fastapi import HTTPException


load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_PORT = os.getenv("LLM_API_PORT")
MODEL_NAME = os.getenv("MODEL_NAME")

FULL_API_URL = f"{LLM_API_URL}:{LLM_API_PORT}/api/generate"


def generate_response(prompt: str, stream: bool = False) -> str:
    payload = {
        "prompt": prompt,
        "stream": stream,
        "model": MODEL_NAME
    }
    
    try:
        response = requests.post(FULL_API_URL, json=payload)
        response.raise_for_status()  
        return response.text 
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get response from LLM: {e}")