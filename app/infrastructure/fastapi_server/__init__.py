import os
import time

import socketio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
cors = ["*"]

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")

views_dir = os.path.join(os.path.dirname(__file__), "views")

app.mount(
    "/static", StaticFiles(directory=os.path.join(views_dir, "static")), name="static"
)
app.mount("/ws", socketio.ASGIApp(sio, socketio_path="/"))
templates = Jinja2Templates(directory=os.path.join(views_dir, "templates"))

last_time = time.time()


@app.get("/")
async def root():
    return {"ws": "find"}


@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/greet")
async def greet():
    return {"message": "hello world"}


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
