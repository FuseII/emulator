from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
import uvicorn

from app.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory=r'D:\Artem\Magistrature\1_sem\Software_arch\my_labs\emulator\app\static'), 'static')


@app.get("/")
def home_page():
    return RedirectResponse(url="/pages/task_1")
    # return {"message": "Привет, Хабр!"}


app.include_router(router_pages)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
    uvicorn.run(app, host="127.0.0.1", port=5000)