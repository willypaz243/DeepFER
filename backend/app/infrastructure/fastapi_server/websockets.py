import cv2
import numpy as np
import socketio

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")


def proccess_frame(data: bytes) -> tuple:
    """
    Processes a frame received from the client.
    Args:
        data (bytes): The frame received from the client.

    Returns:
        tuple: A tuple containing the shape of the processed frame.
    """
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return frame.shape


@sio.on("connect")
async def connect(sid: str, env):
    """
    Handles a client connection event.

    Args:
        sid (str): The session ID of the connected client.
        env: Environment variables passed to the server.
    """
    print(f"New Client Connected to This id: {sid}")


@sio.on("video_frame")
async def my_message(sid: str, data: bytes):
    """
    Handles a video frame event.

    Args:
        sid (str): The session ID of the client sending the frame.
        data (bytes): The frame received from the client.

    Emits:
        dict: A dictionary containing the processed frame and its shape.
    """
    shape = proccess_frame(data)
    await sio.emit("video_frame", dict(data=data, shape=shape), skip_sid=sid)


@sio.on("disconnect")
async def disconnect(sid: str):
    """
    Handles a client disconnection event.

    Args:
        sid (str): The session ID of the disconnected client.
    """
    print(f"Client Disconnected: {sid}")
