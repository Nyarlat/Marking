import json
import os
import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from app.services.marking import get_random_row


router = APIRouter(prefix="/marking",
                   tags=["marking"])

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/load")
async def load_marking(file: UploadFile):
    file_name = f"image_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {"filename": file_name, "file_path": file_path}
    except Exception as e:
        return {"error": str(e)}

