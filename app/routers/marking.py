from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.services.marking import get_random_row


router = APIRouter(prefix="/marking",
                   tags=["marking"])


@router.post("/load")
async def load_marking(file: UploadFile):
    component = get_random_row()
    return component
