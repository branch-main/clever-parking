import base64
import os
from datetime import datetime

from .config import CAPTURES_DIR, PREDICTIONS_DIR


def save_image(image_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"capture_{timestamp}.jpg"
    filepath = os.path.join(CAPTURES_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_data)

    print(f"Saved: {filename} ({len(image_data)} bytes)")
    return filename, timestamp


def save_label_visualization(label_visualization_b64, timestamp):
    try:
        if not label_visualization_b64:
            print("Warning: label_visualization is None or empty")
            return
            
        print(f"Saving label visualization (length: {len(label_visualization_b64)} chars)")
        image_data = base64.b64decode(label_visualization_b64)
        prediction_filename = f"prediction_{timestamp}.jpg"
        prediction_filepath = os.path.join(PREDICTIONS_DIR, prediction_filename)

        with open(prediction_filepath, "wb") as f:
            f.write(image_data)

        print(f"Saved prediction: {prediction_filename} ({len(image_data)} bytes)")

    except Exception as e:
        print(f"Error saving prediction image: {str(e)}")
        import traceback
        traceback.print_exc()
