from fastapi import APIRouter, HTTPException, Request
import handler.end_life_preference_handler as elp_handler
from utils.logger_factory import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/user/{user_id}/end_life_preferences", tags=['end_life_preferences'])

@router.get("/")
async def get_end_life_preferences(user_id: str):
    preferences = elp_handler.find(user_id)
    if preferences:
        return preferences
    raise HTTPException(status_code=404, detail="End-of-life preferences not found")

@router.post("/")
async def create_end_life_preferences(user_id: str, request: Request):
    body = await request.json()
    created_preferences = elp_handler.create(user_id, body)
    logger.info(created_preferences)
    if created_preferences:
        return created_preferences
    raise HTTPException(status_code=400, detail="Failed to create end-of-life preferences")

@router.put("/")
async def update_end_life_preferences(user_id: str, request: Request):
    body = await request.json()
    updated_preferences = elp_handler.update(user_id, body)
    if updated_preferences:
        return updated_preferences
    raise HTTPException(status_code=400, detail="Failed to update end-of-life preferences")

@router.delete("/")
async def delete_end_life_preferences(user_id: str):
    deleted_preferences = elp_handler.delete(user_id, end_life_preferences_id="")
    if deleted_preferences:
        return deleted_preferences
    raise HTTPException(status_code=400, detail="Failed to delete end-of-life preferences")
