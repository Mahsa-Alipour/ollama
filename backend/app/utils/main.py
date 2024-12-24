# app/main.py

from fastapi import FastAPI
from app.routers import qa, resume_summarizer, image_describer

app = FastAPI(title="Llava-Llama3 Multi Modal API")

# Include routers
app.include_router(qa.router)
app.include_router(resume_summarizer.router)
app.include_router(image_describer.router)
