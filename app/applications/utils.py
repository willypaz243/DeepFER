import base64

import cv2
import numpy as np

from .deepfed import FedPredictor

DFERP = FedPredictor()
LABELS = ['Feliz', 'Neutral', 'Triste', 'Enfado', 'Asco', 'Sorpresa', 'Miedo']


def from_base64_to_cv2_image(buf) -> np.ndarray:
    buf_decode = base64.b64decode(buf)
    buf_arr: np.ndarray = np.frombuffer(buf_decode, dtype=np.uint8)
    return cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)


def analize_img_to_feeling(img_base64: str):
    _, content = img_base64.split(',')
    img = from_base64_to_cv2_image(content)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, prediction = DFERP.predict_one(gray)
    feeling = []
    if prediction is not None:
        prediction = (100 * prediction).astype(int)
    for i, label in enumerate(LABELS):
        feeling.append({'label': label, 'value': int(prediction[i]) if prediction is not None else 0})
    return feeling, prediction
