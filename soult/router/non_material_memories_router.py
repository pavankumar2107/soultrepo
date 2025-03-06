from fastapi import APIRouter, HTTPException, Request
import handler.non_material_memories_handler as non_material_memory_handler

router = APIRouter(prefix="/user/{user_id}/non_material_memory", tags=["non_material_memory"])

@router.get("/{non_material_memory_id}")
async def get_non_material_memory(user_id: str, non_material_memory_id: str):
    memory = non_material_memory_handler.find(user_id, non_material_memory_id)
    if memory:
        return memory
    raise HTTPException(status_code=404, detail="Non-material memory not found")

@router.get("/")
async def get_all_non_material_memories(user_id: str):
    memories = non_material_memory_handler.find_all(user_id)
    if memories:
        return memories
    raise HTTPException(status_code=404, detail="No non-material memories found for this user")

@router.post("/")
async def create_non_material_memory(user_id: str, request: Request):
    body = await request.json()
    created_memory = non_material_memory_handler.create(user_id, body)
    if created_memory:
        return created_memory
    raise HTTPException(status_code=400, detail="Non-material memory creation failed")

@router.put("/{non_material_memory_id}")
async def update_non_material_memory(user_id: str, non_material_memory_id: str, request: Request):
    body = await request.json()
    updated_memory = non_material_memory_handler.update(user_id, non_material_memory_id, body)
    if updated_memory:
        return updated_memory
    raise HTTPException(status_code=400, detail="Non-material memory update failed")

@router.delete("/{non_material_memory_id}")
async def delete_non_material_memory(user_id: str, non_material_memory_id: str):
    deleted_memory = non_material_memory_handler.delete(user_id, non_material_memory_id)
    if deleted_memory:
        return deleted_memory
    raise HTTPException(status_code=400, detail="Non-material memory deletion failed")
