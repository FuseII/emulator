from fastapi import FastAPI, Response, Request
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
import uvicorn

from app.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_credentials=True,
#                    allow_methods=["*"])

app.mount('/static', StaticFiles(directory=r'D:\Artem\Magistrature\1_sem\Software_arch\my_labs\emulator\app\static'),
          'static')



@app.get("/")
def home_page():
    return RedirectResponse(url="/pages/task_1")
    # return {"message": "Привет, Хабр!"}


app.include_router(router_pages)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
