from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_utils import compute_similarity
from pypdf import PdfReader
import io
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resume_screener")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/ping")
def ping():
    return {"msg": "ok"}

# Request model
class MatchRequest(BaseModel):
    job_description: str
    resumes: list[str]

# Match endpoint
@app.post("/match")
def match_resumes(data: MatchRequest):
    try:
        jd = data.job_description
        resumes = data.resumes
        results = compute_similarity(jd, resumes)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PDF Upload Endpoint
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        content = await file.read()
        pdf = PdfReader(io.BytesIO(content))

        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return {"filename": file.filename, "text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 