from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.pdf_processor import extract_text_from_pdf
from app.utils.resumellm_client import generate_response

router = APIRouter()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ask_pdf")
async def ask_pdf(prompt: str = Form(...), file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    try:
        # Save the uploaded PDF
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="No text extracted from the PDF")

        # Combine the prompt with the extracted text
        combined_prompt = f"{prompt}\n\nExtracted Text:\n{text}"

        # Generate response from LLM
        response = generate_response(combined_prompt)

        # Ensure the response is a dictionary and contains the expected fields
        if not isinstance(response, dict) or "response" not in response:
            raise HTTPException(status_code=500, detail="Invalid response format from LLM")

        return JSONResponse(content=response)
    finally:
        # Clean up the file
        if os.path.exists(file_path):
            os.remove(file_path)
