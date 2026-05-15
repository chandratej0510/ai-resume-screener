import logging
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.models import MatchResponse
from app.services.pdf_parser import extract_text_from_pdf
from app.services.matcher import compute_similarity

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/match", response_model=MatchResponse)
async def match_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    parsed_resumes = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Only PDF files allowed. {file.filename} is not a PDF.")
        
        try:
            text = await extract_text_from_pdf(file)
            parsed_resumes.append({
                "filename": file.filename,
                "text": text
            })
        except Exception as e:
            logger.error(f"Failed to process {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process {file.filename}")

    try:
        results = compute_similarity(job_description, parsed_resumes)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error during matching: {e}")
        raise HTTPException(status_code=500, detail="Error computing similarity")
