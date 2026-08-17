import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Load and preprocess MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize pixel values between 0 and 1, and reshape to (28, 28, 1)
x_train = x_train.reshape((-1, 28, 28, 1)).astype('float32') / 255.0
x_test = x_test.reshape((-1, 28, 28, 1)).astype('float32') / 255.0

# 2. Build the CNN Architecture
model = models.Sequential([
    # First Convolutional + Pooling Layer
    layers.Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    # Second Convolutional + Pooling Layer
    layers.Conv2D(64, (5, 5), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # Fully Connected (Dense) Layers
    layers.Flatten(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# 3. Compile the Model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 4. Train the Model
print("Training CNN model...")
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

# 5. Evaluate Accuracy
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"\nFinal Test Accuracy: {test_acc * 100:.2f}%")

# 6. Save Trained Model
model.save('mnist_cnn_model.keras')
print("Model successfully saved to mnist_cnn_model.keras")
