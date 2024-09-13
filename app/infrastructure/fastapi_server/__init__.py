import os
import time

import socketio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.v1 import router as v1_router

app = FastAPI()
cors = ["*"]

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")

views_dir = os.path.join(os.path.dirname(__file__), "views")

app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/ws", socketio.ASGIApp(sio, socketio_path="/"))
templates = Jinja2Templates(directory="dist")

last_time = time.time()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@sio.on("connect")
async def connect(sid, env):
    print("New Client Connected to This id :" + " " + str(sid))


@sio.on("message")
async def my_message(sid, data):
    global last_time
    print("message ", data, f"{(time.time() - last_time):2f}")
    last_time = time.time()


@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: " + " " + str(sid))


# Api routes
app.include_router(v1_router, prefix="/api", tags=["v1"])
