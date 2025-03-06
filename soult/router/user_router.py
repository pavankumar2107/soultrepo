import json
import logging
from fastapi import APIRouter, HTTPException, Request, Query, UploadFile, File, Form
import handler.user_handler as user_handler
from handler.file_to_s3 import upload_file_to_s3
from utils.response_utils import build_response

router = APIRouter(prefix="/user", tags=['user'])


@router.get("/phone")
async def find_phone(phone_number: str = Query(None)):
    logging.info(phone_number)
    if phone_number is None:
        raise HTTPException(status_code=400, detail="phone_number is required")
    exists = user_handler.find_phone(phone_number)
    return {"exists": exists}

@router.get("/email")
async def find_email(email: str = Query(None)):
    logging.info(email)
    if email is None:
        raise HTTPException(status_code=400, detail="email is required")
    exists = user_handler.find_email(email)
    return {"exists": exists}

@router.get("/{user_id}")
async def get_user(user_id: str):
    user = user_handler.find(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/cognito/{user_id}")
async def get_user(user_id: str):
    user = user_handler.validate(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/")
async def create_user(request: Request):
    body = await request.json()
    created_user = user_handler.create(body)
    if created_user:
        return created_user
    raise HTTPException(status_code=400, detail="User creation failed")

@router.put("/{user_id}")
async def update_user(user_id: str, request: Request):
    body = await request.json()
    updated_user = user_handler.update(user_id, body)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=400, detail="User update failed")

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    deleted_user = user_handler.delete(user_id, model_id="user")
    if deleted_user:
        return deleted_user
    raise HTTPException(status_code=400, detail="User deletion failed")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), metadata: str = Form(...)):
    file_content = await file.read()
    metadata_dict = json.loads(metadata)
    if 'user_id' not in metadata_dict:
        return build_response({'error': "Invalid User_Id"})
    user_id = metadata_dict.get("user_id")
    file_name = f"{user_id}/{file.filename}"
    response = upload_file_to_s3(file_name, user_id, file_content)
    return build_response(response)