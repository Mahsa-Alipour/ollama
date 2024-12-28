import subprocess
from fastapi import HTTPException

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

