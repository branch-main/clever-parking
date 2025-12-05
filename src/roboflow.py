import base64

import requests

from .config import ROBOFLOW_API_KEY, ROBOFLOW_API_URL


def predict_image(image_data):
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    payload = {
        "api_key": ROBOFLOW_API_KEY,
        "inputs": {"image": {"type": "base64", "value": image_base64}},
    }

    response = requests.post(ROBOFLOW_API_URL, json=payload, timeout=30)
    if response.status_code != 200:
        raise Exception(f"Roboflow API error: {response.status_code} - {response.text}")

    return response.json()
