import requests
from fastapi import HTTPException

def generate_response_with_image(prompt: str, image_data: bytes) -> dict:
    """
    Sends a prompt and image data to the LLM API and returns the JSON response.
    """
    try:
        # Send the prompt and image to the LLM API
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",  # Update the endpoint as needed
            json={
                "prompt": prompt,
                "stream": False,
                "model": "llava-llama3:latest",
                "image": image_data.hex()  # Convert binary image to hex format
            }
        )

        if response.status_code == 200:
            return response.json()  # Return the parsed JSON response
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get response from LLM: {response.text}"
            )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while contacting LLM: {str(e)}")
