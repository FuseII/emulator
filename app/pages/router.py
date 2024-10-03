from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.templating import Jinja2Templates

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

@router.post('/calculate')
async def calculate(data):
    return {"message": data}
