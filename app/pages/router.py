from typing import List

from fastapi import APIRouter, Request, Depends, UploadFile, Response, Body
from fastapi.exceptions import ValidationException, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.exceptions import CommandException
from app.service.code_analyzer import initialization, next_step,reset, run_all, REGISTERS, DATA, PROGRAM_MEMORY, PROGRAM_FINISHED

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


class Data(BaseModel):
    array: List[int]
    text: str




@router.post('/enter_data')
async def enter_data(data: Data):
    message = f"Массив размера {len(data.array)} с элементами {data.array} успешно загружен в память"
    initialization(array=data.array,code=data.text)
    print("DATA_MEMORY = {}".format(DATA))
    return {"status": 200, "message": message}




@router.get('/next_step')
async def step(request: Request):
    try:
        result = next_step()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    finished = result.get('finished')
    message = result.get('message')
    if finished:
        print("!!!Программа завершена")
    return {"status": 200, "message": message, "program_finished":finished}


@router.get('/reset')
async def reset_data(request: Request):
    try:
        reset()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    message = f"Команда выполнена успешно"
    return {"status": 200, "message": message}

@router.get('/run_all')
async def run_all_program(request: Request):
    try:
        run_all()
    except CommandException as exc:
        print(exc.msg)
        raise HTTPException(status_code=404, detail=exc.msg)
    message = f"Команда выполнена успешно"
    return {"status": 200, "message": message}