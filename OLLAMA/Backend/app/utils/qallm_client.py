import requests
from fastapi import HTTPException

LLM_API_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llava-llama3:latest"

def generate_response(prompt: str, stream: bool = False) -> str:
    payload = {
        "prompt": prompt,
        "stream": stream,
        "model": MODEL_NAME
    }
    
    try:
        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text  # Return the raw text response
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get response from LLM: {e}")
