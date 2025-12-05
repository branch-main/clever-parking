from flask import Blueprint, jsonify, request, render_template, send_from_directory
import os
import glob

from .roboflow import predict_image
from .slot_processor import SlotProcessor
from .utils import save_image, save_label_visualization
from .config import CAPTURES_DIR, PREDICTIONS_DIR

api = Blueprint("api", __name__)
slot_processor = SlotProcessor()
flash_state = {"enabled": False}


def get_image_data():
    if "image" not in request.files:
        if request.content_type == "image/jpeg":
            image_data = request.data
            if not image_data:
                return None, jsonify({"error": "No image data"}), 400
        else:
            return None, jsonify({"error": "No image provided"}), 400
    else:
        image_data = request.files["image"].read()
    return image_data, None, None


def get_latest_file(directory, pattern):
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    return os.path.basename(max(files, key=os.path.getctime))


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/images/captures/<path:filename>")
def serve_capture(filename):
    return send_from_directory(CAPTURES_DIR, filename)


@api.route("/images/predictions/<path:filename>")
def serve_prediction(filename):
    return send_from_directory(PREDICTIONS_DIR, filename)


@api.route("/images/captures/latest")
def latest_capture():
    latest = get_latest_file(CAPTURES_DIR, "capture_*.jpg")
    if not latest:
        return jsonify({"error": "No captures available"}), 404
    return send_from_directory(CAPTURES_DIR, latest)


@api.route("/images/predictions/latest")
def latest_prediction():
    latest = get_latest_file(PREDICTIONS_DIR, "prediction_*.jpg")
    if not latest:
        return jsonify({"error": "No predictions available"}), 404
    return send_from_directory(PREDICTIONS_DIR, latest)


@api.route("/status")
def status():
    return jsonify({
        "flash": flash_state["enabled"],
        "slots": slot_processor.last_known_slots
    })


@api.route("/flash/toggle", methods=["POST"])
def toggle_flash():
    flash_state["enabled"] = not flash_state["enabled"]
    return jsonify({"flash": flash_state["enabled"]})


@api.route("/predict", methods=["POST"])
def predict():
    image_data, error, status_code = get_image_data()
    if error:
        return error, status_code

    _, timestamp = save_image(image_data)

    try:
        result = predict_image(image_data)
        predictions_list, label_visualization = slot_processor.extract_data(result)
        slots = slot_processor.process_predictions(predictions_list)

        if label_visualization:
            save_label_visualization(label_visualization, timestamp)

        return jsonify({
            "status": "ok", 
            "slots": slots,
            "flash": flash_state["enabled"]
        }), 200

    except Exception as e:
        print(f"Error calling Roboflow: {str(e)}")
        return jsonify({"error": str(e)}), 500
