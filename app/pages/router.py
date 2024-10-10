from typing import List

from fastapi import APIRouter, Request, Depends, UploadFile, Response, Body
from fastapi.exceptions import ValidationException, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory=r'D:\Artem\Magistrature\1_sem\Software_arch\my_labs\emulator\app\templates')


@router.get('/task_1')
async def task_1(request: Request):
    return templates.TemplateResponse(name='index.html',
                                      context={'request': request})


@router.get('/task_2')
async def task_2(request: Request):
    return {"message": "Hello World"}


@router.get('/about')
async def about(request: Request):
    return templates.TemplateResponse(name='about.html',
                                      context={'request': request})


class Calculate(BaseModel):
    # data: str = Field(..., min_length=1)
    data: List[int]


@router.post('/calculate')
async def calculate(text: Calculate = Body()):
    message = f"Массив размера {len(text.data)} с элементами {text.data} успешно загружен в память"
    return {"status":200,"message": message}
