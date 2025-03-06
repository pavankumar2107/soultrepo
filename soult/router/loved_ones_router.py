from fastapi import APIRouter, HTTPException, Request
import handler.loved_ones_handler as loved_ones_handler

router = APIRouter(prefix="/user/{user_id}/loved_ones", tags=["loved_ones"])

@router.get("/{loved_ones_id}")
async def get_loved_one(user_id: str, loved_ones_id: str):
    loved_one = loved_ones_handler.find(user_id, loved_ones_id)
    if loved_one:
        return loved_one
    raise HTTPException(status_code=404, detail="Loved one not found")

@router.get("/")
async def get_all_loved_ones(user_id: str):
    loved_ones = loved_ones_handler.find_all(user_id)
    if loved_ones:
        return loved_ones
    raise HTTPException(status_code=404, detail="No loved ones found for this user")

@router.post("/")
async def create_loved_one(user_id: str, request: Request):
    body = await request.json()
    created_loved_one = loved_ones_handler.create(user_id, body)
    if created_loved_one:
        return created_loved_one
    raise HTTPException(status_code=400, detail="Loved one creation failed")

@router.put("/{loved_ones_id}")
async def update_loved_one(user_id: str, loved_ones_id: str, request: Request):
    body = await request.json()
    updated_loved_one = loved_ones_handler.update(user_id, loved_ones_id, body)
    if updated_loved_one:
        return updated_loved_one
    raise HTTPException(status_code=400, detail="Loved one update failed")

@router.delete("/{loved_ones_id}")
async def delete_loved_one(user_id: str, loved_ones_id: str):
    deleted_loved_one = loved_ones_handler.delete(user_id, loved_ones_id)
    if deleted_loved_one:
        return deleted_loved_one
    raise HTTPException(status_code=400, detail="Loved one deletion failed")
