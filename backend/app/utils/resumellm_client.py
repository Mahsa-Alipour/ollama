import requests
from fastapi import HTTPException

def generate_response(prompt: str) -> dict:
    """
    Sends a prompt to the LLM API and returns the JSON response.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "prompt": prompt,
                "stream": False,
                "model": "llava-llama3:latest"
            }
        )

        if response.status_code == 200:
            return response.json()  # Ensure it returns a dictionary
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get response from LLM: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while contacting LLM: {str(e)}")
