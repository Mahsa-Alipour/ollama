import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_PORT = os.getenv("LLM_API_PORT")
MODEL_NAME = os.getenv("MODEL_NAME")

FULL_API_URL = f"{LLM_API_URL}:{LLM_API_PORT}/api/generate"

def generate_response(prompt: str) -> dict:
    """
    Sends a prompt to the LLM API and returns the JSON response.
    """
    try:
        response = requests.post(
            FULL_API_URL,
            json={
                "prompt": prompt,
                "stream": False,
                "model": MODEL_NAME
            }
        )

        if response.status_code == 200:
            return response.json()  
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get response from LLM: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while contacting LLM: {str(e)}")



# import os
# import requests
# from fastapi import HTTPException
# from dotenv import load_dotenv
# from app.services.constants import PROMPT_1  

# load_dotenv() 

# LLM_API_URL = os.getenv("LLM_API_URL")
# LLM_API_PORT = os.getenv("LLM_API_PORT")
# MODEL_NAME = os.getenv("MODEL_NAME")

# FULL_API_URL = f"{LLM_API_URL}:{LLM_API_PORT}/api/generate"

# def generate_response(resume_text: str) -> dict:
#     """
#     Constructs the prompt using the resume text, sends it to the LLM API, and returns the JSON response.
#     """
#     prompt = PROMPT_1.format(resume=resume_text)
#     try:
#         response = requests.post(
#             FULL_API_URL,
#             json={
#                 "prompt": prompt,
#                 "stream": False,
#                 "model": MODEL_NAME
#             }
#         )

#         if response.status_code == 200:
#             return response.json()  
#         else:
#             raise HTTPException(
#                 status_code=response.status_code,
#                 detail=f"Failed to get response from LLM: {response.text}"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error while contacting LLM: {str(e)}")