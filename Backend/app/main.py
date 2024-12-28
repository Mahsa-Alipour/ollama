from fastapi import FastAPI
from app.routs import image_describer_endpoint, qa_endpoint
from app.routs import resume_summarizer_endpoint

app = FastAPI(title="Llava-Llama3 Multi Modal API")


app.include_router(
    qa_endpoint.router,
    prefix="/qa",
    tags=["Question Answering"]
)

app.include_router(
    resume_summarizer_endpoint.router,
    prefix="/resume",
    tags=["Resume Summarizer"]
)

app.include_router(
    image_describer_endpoint.router,
    prefix="/image",
    tags=["Image Describer"]
)