import base64
import io

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
from PIL import Image

app = Flask(__name__)

MODEL_PATH = "mnist_cnn_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print(f"Loaded model from {MODEL_PATH}")


def preprocess(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("L")

    img_array = np.array(img)

    # Threshold to clean anti-aliased edges (white digit on black background)
    img_array = np.where(img_array > 50, 255, 0).astype("uint8")

    if img_array.max() == 0:
        return None

    # Find the bounding box of the drawn digit
    ys, xs = np.where(img_array > 0)
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()

    h, w = img_array.shape
    pad = 2
    x_min = max(0, x_min - pad)
    y_min = max(0, y_min - pad)
    x_max = min(w - 1, x_max + pad)
    y_max = min(h - 1, y_max + pad)

    cropped = img_array[y_min : y_max + 1, x_min : x_max + 1]
    crop_img = Image.fromarray(cropped)

    # Fit into 20x20 preserving aspect ratio, then center in 28x28
    crop_img.thumbnail((20, 20), Image.Resampling.LANCZOS)
    canvas = Image.new("L", (28, 28), 0)
    offset = ((28 - crop_img.width) // 2, (28 - crop_img.height) // 2)
    canvas.paste(crop_img, offset)

    processed = np.array(canvas).astype("float32") / 255.0
    return processed


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_bytes = base64.b64decode(data["image"])
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400

    try:
        processed = preprocess(image_bytes)
    except Exception:
        return jsonify({"error": "Could not decode the image."}), 400

    if processed is None:
        return jsonify({"error": "Canvas is empty. Draw a digit first."}), 400

    input_tensor = processed.reshape((1, 28, 28, 1))

    predictions = model.predict(input_tensor, verbose=0)[0]

    predicted = int(np.argmax(predictions))
    confidence = float(predictions[predicted] * 100)
    probabilities = [float(p) for p in predictions]

    return jsonify(
        {
            "prediction": predicted,
            "confidence": confidence,
            "probabilities": probabilities,
            "processed": processed.tolist(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
