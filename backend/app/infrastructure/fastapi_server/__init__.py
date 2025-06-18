import os
import time

import socketio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.v1 import router as v1_router
from .websockets import sio

app = FastAPI()
cors = ["*"]

views_dir = os.path.join(os.path.dirname(__file__), "views")

app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/ws", socketio.ASGIApp(sio, socketio_path="/"))
templates = Jinja2Templates(directory="dist")

last_time = time.time()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Api routes
app.include_router(v1_router, prefix="/api", tags=["v1"])
