from typing import List

from fastapi import APIRouter, Request, Depends, UploadFile, Response, Body
from fastapi.exceptions import ValidationException, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.exceptions import CommandException
from app.service.code_analyzer import initialization, next_step, reset, run_all, REGISTERS, DATA, PROGRAM_MEMORY, \
    PROGRAM_FINISHED

router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory=r'D:\Artem\Magistrature\1_sem\Software_arch\my_labs\emulator\app\templates')


@router.get('/task_1')
async def task_1(request: Request):
    return templates.TemplateResponse(name='base.html.jinja',
                                      context={'request': request})


@router.get('/task_2')
async def task_2(request: Request):
    return templates.TemplateResponse(name='child.html.jinja',
                                      context={'request': request})
    # return {"message": "Hello World"}


@router.get('/about')
async def about(request: Request):
    return templates.TemplateResponse(name='about.html',
                                      context={'request': request})


class Data(BaseModel):
    array: List[int] #данные
    text: str #код
    mode:int #Задача №1 или Задача №2


@router.post('/enter_data')
async def enter_data(data: Data):
    # message = f"Массив размера {len(data.array)} с элементами {data.array} успешно загружен в память"
    result = initialization(array=data.array, code=data.text, mode=data.mode)
    # print("DATA_MEMORY = {}".format(DATA))
    result["status"] = 200
    return result


@router.get('/next_step')
async def step(request: Request):
    try:
        result = next_step()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    if result.get('finished'):
        print("!!!Программа завершена")
    result["status"] = 200
    return result


@router.get('/reset')
async def reset_data(request: Request):
    try:
        result = reset()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    result["status"] = 200
    return result


@router.get('/run_all')
async def run_all_program(request: Request):
    try:
        result = run_all()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    result["status"] = 200
    return result

@router.get("/file/download")
def download_file():
  return FileResponse(path=r'D:\Artem\Magistrature\1_sem\Software_arch\my_labs\emulator\app\report.docx', filename='Отчёт.docx', media_type='multipart/form-data')
