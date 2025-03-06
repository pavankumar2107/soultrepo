from fastapi import APIRouter, HTTPException
from handler.ses_handler import ses_handler

router = APIRouter(prefix="/ses", tags=["SES"])

@router.post("/send-notification")
async def send_notification(event_data: dict):
    response = ses_handler(event_data)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response)
    return response
