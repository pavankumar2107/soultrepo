from fastapi import APIRouter, HTTPException, Request
import handler.organ_donation_preferences_handler as organ_donation_handler

router = APIRouter(prefix="/user/{user_id}/organ_donation", tags=['organ_donation'])

@router.get("/{organ_donation_preference_id}")
async def get_organ_donation_preference(user_id: str, organ_donation_preference_id: str):
    preference = organ_donation_handler.find(user_id, organ_donation_preference_id)
    if preference:
        return preference
    raise HTTPException(status_code=404, detail="Organ donation preference not found")

@router.get("/")
async def get_all_organ_donation_preferences(user_id: str):
    preferences = organ_donation_handler.find_all(user_id)
    if preferences:
        return preferences
    raise HTTPException(status_code=404, detail="No organ donation preferences found for this user")

@router.post("/")
async def create_organ_donation_preference(user_id: str, request: Request):
    body = await request.json()
    created_preference = organ_donation_handler.create(user_id, body)
    if created_preference:
        return created_preference
    raise HTTPException(status_code=400, detail="Organ donation preference creation failed")

@router.put("/{organ_donation_preference_id}")
async def update_organ_donation_preference(user_id: str, organ_donation_preference_id: str, request: Request):
    body = await request.json()
    updated_preference = organ_donation_handler.update(user_id, organ_donation_preference_id, body)
    if updated_preference:
        return updated_preference
    raise HTTPException(status_code=400, detail="Organ donation preference update failed")

@router.delete("/{organ_donation_preference_id}")
async def delete_organ_donation_preference(user_id: str, organ_donation_preference_id: str):
    deleted_preference = organ_donation_handler.delete(user_id, organ_donation_preference_id)
    if deleted_preference:
        return deleted_preference
    raise HTTPException(status_code=400, detail="Organ donation preference deletion failed")
