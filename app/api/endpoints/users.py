import os
import shutil
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse
from app.models.users import User


router = APIRouter()


@router.post("/api/")
async def user_create(item: User):
    return item


@router.post("/api/image")
async def post_image(req: Request, file: UploadFile = File(...)):
    print(os.getcwd())
    with open('../media/' + file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return req.base_url.netloc + f'/api/image/{file.filename}'


@router.get("/api/image/{filename}")
async def image_endpoint(filename: str):
    return FileResponse(f'{os.getcwd()}/../media/{filename}')
