from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.pdf_processor import extract_text_from_pdf
from app.services.resume_summarizer import generate_response
router = APIRouter()

UPLOAD_DIR = "./uploads"
MAX_FILE_SIZE = 3 * 1024 * 1024  
ALLOWED_FILE_TYPE = "application/pdf"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ask_pdf")
async def ask_pdf(prompt: str = Form(...), file: UploadFile = File(...)):

    if file.content_type != ALLOWED_FILE_TYPE:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File is too large. Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB.")
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="No text extracted from the PDF")

        combined_prompt = f"{prompt}\n\nExtracted Text:\n{text}"

        response = generate_response(combined_prompt)

        if not isinstance(response, dict) or "response" not in response:
            raise HTTPException(status_code=500, detail="Invalid response format from LLM")

        return JSONResponse(content=response)
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# from fastapi import APIRouter, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# import shutil
# import os
# from app.utils.pdf_processor import extract_text_from_pdf
# from app.services.resume_summarizer import generate_response
# from app.schemas.output_schema import ResumeSummary  
# import json

# router = APIRouter()

# UPLOAD_DIR = "./uploads"
# MAX_FILE_SIZE = 3 * 1024 * 1024  
# ALLOWED_FILE_TYPE = "application/pdf"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/ask_pdf", response_model=ResumeSummary)
# async def ask_pdf(file: UploadFile = File(...)):
#     if file.content_type != ALLOWED_FILE_TYPE:
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

#     contents = await file.read()
#     if len(contents) > MAX_FILE_SIZE:
#         raise HTTPException(status_code=400, detail=f"File is too large. Maximum allowed size is {MAX_FILE_SIZE // (1024 * 1024)} MB.")

#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     try:
#         with open(file_path, "wb") as buffer:
#             buffer.write(contents)

#         text = extract_text_from_pdf(file_path)
#         if not text:
#             raise HTTPException(status_code=400, detail="No text extracted from the PDF")

#         response = generate_response(text)

#         if not isinstance(response, dict):
#             raise HTTPException(status_code=500, detail="Invalid response format from LLM")

#         try:
#             resume_summary = ResumeSummary(**response)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Response validation failed: {str(e)}")

#         return resume_summary

#     finally:
#         if os.path.exists(file_path):
#             os.remove(file_path)