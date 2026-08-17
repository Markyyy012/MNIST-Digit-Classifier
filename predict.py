import tensorflow as tf
import numpy as np

# 1. Load the saved model from disk
print("Loading saved model...")
model = tf.keras.models.load_model('mnist_cnn_model.keras')

# 2. Load test dataset to grab sample images
(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 3. Pick 5 random images from the test set to evaluate
indices = np.random.choice(len(x_test), 5, replace=False)

print("\n--- Model Predictions ---")
for idx in indices:
    image = x_test[idx]
    actual_label = y_test[idx]
    
    # Reshape and normalize image to match model input shape: (1, 28, 28, 1)
    input_tensor = image.reshape((1, 28, 28, 1)).astype('float32') / 255.0
    
    # Predict probabilities across the 10 digit classes
    predictions = model.predict(input_tensor, verbose=0)
    predicted_label = np.argmax(predictions)
    confidence = np.max(predictions) * 100
    
    print(f"Index {idx:4d} | Actual: {actual_label} | Predicted: {predicted_label} | Confidence: {confidence:.2f}%")
