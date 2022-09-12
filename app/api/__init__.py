import os
import base64
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status

from app.api.utils import analize_img_to_feeling, LABELS

router = APIRouter()

CSV_PATH = 'history.csv'


class InterviewConnection:
    def __init__(self) -> None:
        self.interview: WebSocket = None
        self.history = np.empty((0, 7), int)

    async def connect(self, websocket: WebSocket):
        self.interview = websocket

    async def disconnect(self):
        self.interview = None

    async def send_analysis(self, data):
        if (self.interview is not None):
            await self.interview.send_json(data)

    def add_prediction(self, prediction):
        if (prediction is not None):
            self.history = np.append(self.history, [prediction], axis=0)

    def save_history(self):
        df = pd.DataFrame(data=self.history, columns=LABELS)
        df.to_csv(CSV_PATH, index=False)
        self.history = np.empty((0, 7), int)


interview = InterviewConnection()


@router.websocket("/ws/interview")
async def applicantWS(websocket: WebSocket):
    await websocket.accept()
    await interview.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            res, prediction = analize_img_to_feeling(data['data'])
            await interview.send_analysis(res)
            interview.add_prediction(prediction)
    except WebSocketDisconnect:
        await interview.disconnect()
        interview.save_history()


@router.get('/feeling_report')
async def get_feeling_report():
    if (not os.path.exists(CSV_PATH)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    df = pd.read_csv(CSV_PATH)
    df.plot(subplots=True, figsize=(20, 10), layout=(4, 2), ylim=(0, 100))
    plt.tight_layout()
    my_stringIObytes = BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    return {'data': my_base64_jpgData}
