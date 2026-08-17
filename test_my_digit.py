import numpy as np
import tensorflow as tf
from PIL import Image

# 1. Load model
model = tf.keras.models.load_model('mnist_cnn_model.keras')

# 2. Open and preprocess image
image_path = 'image.png'

try:
    img = Image.open(image_path).convert('L')
    img = img.resize((28, 28), Image.Resampling.LANCZOS)
    img_array = np.array(img)

    # Invert if background is white
    if np.mean(img_array) > 127:
        img_array = 255 - img_array

    # Boost contrast (make lines solid white)
    img_array = np.where(img_array > 50, 255, 0).astype('uint8')

    # Normalize for prediction
    input_tensor = img_array.astype('float32') / 255.0
    input_tensor = input_tensor.reshape((1, 28, 28, 1))

    # 3. Print mini ASCII view in terminal to inspect what the model sees
    print("\nHow the model sees your drawing (28x28):")
    for row in img_array:
        line = "".join(["#" if pixel > 128 else " " for pixel in row])
        print(line)

    # 4. Predict
    predictions = model.predict(input_tensor, verbose=0)
    predicted_digit = np.argmax(predictions)
    confidence = np.max(predictions) * 100

    print("\n=========================")
    print(f"  Predicted Digit: {predicted_digit}")
    print(f"  Confidence:     {confidence:.2f}%")
    print("=========================\n")

except FileNotFoundError:
    print(f"Error: Could not find '{image_path}'")
