import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from dotenv import load_dotenv
from app.core.processing import process_meeting_input, save_minutes_to_word
from app.schemas.model import MeetingMinutes
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure outputs directory exists
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

class ProcessingRequest(BaseModel):
    text: str

@app.post("/process/text")
async def process_text(file: Optional[UploadFile] = None, text: Optional[str] = Form(None)):
    try:
        if file:
            content = await file.read()
            input_text = content.decode()
        elif text:
            input_text = text
        else:
            raise HTTPException(status_code=400, detail="Either file or text must be provided")
            
        minutes = process_meeting_input(input_text, "text")
        filename = save_minutes_to_word(minutes)
        return {"minutes": minutes.dict(), "download_url": f"/download/{filename}"}
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/audio")
async def process_audio(file: UploadFile):
    try:
        logger.info(f"Received audio file: {file.filename}")
        temp_file = f"/tmp/{uuid.uuid4()}"
        
        # Save uploaded file
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)
            logger.info(f"Saved file to {temp_file}")
        
        try:
            # Process the meeting input
            minutes = process_meeting_input(temp_file, "audio")
            logger.info("Successfully processed meeting input")
            
            # Save to word document
            filename = save_minutes_to_word(minutes)
            logger.info(f"Saved minutes to {filename}")
            
            return {"minutes": minutes.dict(), "download_url": f"/download/{filename}"}
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                logger.info(f"Cleaned up temp file: {temp_file}")
                
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        file_path = OUTPUT_DIR / filename
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"Serving file: {file_path}")
        return FileResponse(
            path=str(file_path),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))