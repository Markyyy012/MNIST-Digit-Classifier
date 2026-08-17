<<<<<<< HEAD
# MNIST CNN Digit Classifier

A convolutional neural network that classifies handwritten digits (0-9) from the MNIST dataset, with an interactive web interface for drawing digits and getting real-time predictions.

## Tech Stack

- **TensorFlow / Keras** — model training and inference
- **Flask** — lightweight Python web backend
- **HTML5 Canvas / CSS / JavaScript** — interactive drawing front end
- **Pillow / NumPy** — image preprocessing

## Features

### Interactive Web Interface

- Draw a digit (0-9) on a responsive canvas with mouse or touch (mobile/tablet support)
- **Test My Digit** — sends the drawing to the server for prediction
- **Clear Canvas** — resets for a new drawing
- Results display:
  - Predicted digit and confidence score
  - Probability bar chart across all 10 classes
  - 28×28 processed thumbnail showing exactly what the model sees

### Command-Line Scripts

- `predict.py` — predict 5 random MNIST test images
- `test_my_digit.py` — predict a single hand-drawn image (`image.png`) with an ASCII preview

## Model Architecture

```
Conv2D(32, 5x5, relu) -> MaxPool2D(2x2) -> Conv2D(64, 5x5, relu) -> MaxPool2D(2x2)
-> Flatten -> Dense(1024, relu) -> Dropout(0.5) -> Dense(10, softmax)
```

- **Optimizer:** Adam
- **Loss:** sparse categorical crossentropy
- **Input:** grayscale image, shape `(28, 28, 1)`, normalized to `[0, 1]`

## Project Structure

```
mnist/
├── app.py                 # Flask backend (serves UI + /predict API)
├── train.py               # Train and save the CNN
├── predict.py             # Predict random test images
├── test_my_digit.py       # Predict a hand-drawn image
├── mnist_cnn_model.keras  # Trained model
├── templates/
│   └── index.html         # Web UI
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
└── setup.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Markyyy012/MNIST-Digit-Classifier.git
cd MNIST-Digit-Classifier
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the web app

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser, draw a digit, and click **Test My Digit**.

### 5. (Optional) Run the CLI scripts

```bash
python predict.py        # Predict 5 random test images
python test_my_digit.py  # Predict the digit in image.png
```

## Retraining the Model

To retrain the model from scratch (5 epochs, batch size 64):

```bash
python train.py
```

This downloads the MNIST dataset, trains the CNN, prints the final test accuracy, and overwrites `mnist_cnn_model.keras`.

## Notes

- The model file (~13 MB) is committed directly to the repository (under GitHub's 50 MB warning limit). Consider Git LFS if the model grows larger.
- The backend preprocesses drawings using standard MNIST conventions: grayscale conversion, thresholding, bounding-box cropping, and centering the digit in a 28×28 canvas.
=======
# MNIST-Digit-Classifier
>>>>>>> 704cde64cfd2efc4107dd77b0f8ba4de56f0b303
