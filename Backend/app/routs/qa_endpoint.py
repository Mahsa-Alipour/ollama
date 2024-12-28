from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services.qa import generate_response

router = APIRouter()

@router.get("/ask_text")
def ask_text(prompt: str):
    try:
        res_text = generate_response(prompt, stream=False)
        return Response(content=res_text, media_type="application/json")
    except HTTPException as he:
        
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")