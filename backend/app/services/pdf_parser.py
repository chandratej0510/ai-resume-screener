import io
import logging
from pypdf import PdfReader
from fastapi import UploadFile

logger = logging.getLogger(__name__)

async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text content from an uploaded PDF file asynchronously.
    """
    try:
        content = await file.read()
        pdf = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF {file.filename}: {e}")
        raise ValueError(f"Could not parse PDF: {file.filename}")
