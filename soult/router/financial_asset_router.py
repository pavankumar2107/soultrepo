from fastapi import APIRouter, HTTPException, Request
import handler.financial_asset_handler as financial_asset_handler

router = APIRouter(prefix="/user/{user_id}/financial_asset", tags=['financial_asset'])

@router.get("/{financial_asset_id}")
async def get_financial_asset(user_id: str, financial_asset_id: str):
    asset = financial_asset_handler.find(user_id, financial_asset_id)
    if asset:
        return asset
    raise HTTPException(status_code=404, detail="Financial asset not found")

@router.get("/")
async def get_all_financial_assets(user_id: str):
    assets = financial_asset_handler.find_all(user_id)
    if assets:
        return assets
    raise HTTPException(status_code=404, detail="No financial assets found for this user")

@router.post("/")
async def create_financial_asset(user_id: str, request: Request):
    body = await request.json()
    created_asset = financial_asset_handler.create(user_id, body)
    if created_asset:
        return created_asset
    raise HTTPException(status_code=400, detail="Financial asset creation failed")

@router.put("/{financial_asset_id}")
async def update_financial_asset(user_id: str, financial_asset_id: str, request: Request):
    body = await request.json()
    updated_asset = financial_asset_handler.update(user_id, financial_asset_id, body)
    if updated_asset:
        return updated_asset
    raise HTTPException(status_code=400, detail="Financial asset update failed")

@router.delete("/{financial_asset_id}")
async def delete_financial_asset(user_id: str, financial_asset_id: str):
    deleted_asset = financial_asset_handler.delete(user_id, financial_asset_id)
    if deleted_asset:
        return deleted_asset
    raise HTTPException(status_code=400, detail="Financial asset deletion failed")
