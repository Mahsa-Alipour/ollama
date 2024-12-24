from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.imagellm_client import generate_response_with_image

router = APIRouter()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the upload directory exists

@router.post("/ask_image")
async def ask_image(prompt: str = Form(...), file: UploadFile = File(...)):
    """
    Handles image uploads and queries the LLM for a response.
    """
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    try:
        # Save the uploaded image locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read the binary data of the image
        with open(file_path, "rb") as img_file:
            img_data = img_file.read()

        # Generate a response from the LLM client
        response = generate_response_with_image(prompt, img_data)

        # Validate and return the response from the LLM client
        if not isinstance(response, dict) or "response" not in response:
            raise HTTPException(status_code=500, detail="Invalid response format from LLM")

        return JSONResponse(content=response)
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
