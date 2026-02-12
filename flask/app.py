import numpy as np
import os
from flask import Flask, request, render_template
from PIL import Image

app = Flask(__name__)

# Try to load model with TensorFlow Lite first (for Vercel), then fall back to Keras
model = None
interpreter = None
model_path = os.path.join(os.path.dirname(__file__), "vegetable_classification.h5")
tflite_model_path = os.path.join(os.path.dirname(__file__), "vegetable_classification.tflite")

# Try TensorFlow Lite first (for production/Vercel)
try:
    import tflite_runtime.interpreter as tflite
    if os.path.exists(tflite_model_path):
        interpreter = tflite.Interpreter(model_path=tflite_model_path)
        interpreter.allocate_tensors()
        print("TensorFlow Lite model loaded successfully!")
    else:
        print(f"TFLite model not found at {tflite_model_path}")
except ImportError:
    print("TensorFlow Lite runtime not available, trying Keras...")

# Fall back to Keras if TFLite not available (for local development)
if interpreter is None:
    try:
        from keras.models import load_model
        if os.path.exists(model_path):
            model = load_model(model_path, compile=False)
            print("Keras model loaded successfully!")
        else:
            print(f"Warning: Model file not found at {model_path}")
            print("Please train the model using the Jupyter notebook first.")
    except ImportError:
        print("Neither TensorFlow Lite nor Keras is available.")

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    img = Image.open(img_path).convert('RGB')
    img = img.resize((299, 299))
    img_arr = np.array(img, dtype=np.float32)
    img_arr = np.expand_dims(img_arr, axis=0)
    return img_arr

def predict_with_model(img_input):
    """Make prediction using available model (TFLite or Keras)"""
    if interpreter is not None:
        # Use TensorFlow Lite
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], img_input)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        return np.argmax(output_data)
    elif model is not None:
        # Use Keras
        return np.argmax(model.predict(img_input))
    else:
        return None

# Default home page or route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction.html')
def prediction():
    return render_template('prediction.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

@app.route('/result', methods=["GET", "POST"])
def res():
    if request.method == "POST":
        if model is None and interpreter is None:
            return render_template('prediction.html', pred="Model not loaded! Please train the model first.")
        
        f = request.files['image']
        basepath = os.path.dirname(__file__)  # Getting the current path i.e where app.py is present
        filepath = os.path.join(basepath, 'uploads', f.filename)  # Store anywhere in the system we can give image but we want that in uploads folder
        
        # Create uploads directory if it doesn't exist
        os.makedirs(os.path.join(basepath, 'uploads'), exist_ok=True)
        f.save(filepath)
        
        # Preprocess and predict
        img_input = preprocess_image(filepath)
        pred = predict_with_model(img_input)
        
        if pred is None:
            return render_template('prediction.html', pred="Error: Unable to make prediction")
        
        # Class mapping
        op = {
            0: 'Bean', 
            1: 'Bitter_Gourd', 
            2: 'Bottle_Gourd', 
            3: 'Brinjal', 
            4: 'Broccoli', 
            5: 'Cabbage', 
            6: 'Capsicum', 
            7: 'Carrot', 
            8: 'Cauliflower', 
            9: 'Cucumber', 
            10: 'Papaya', 
            11: 'Potato', 
            12: 'Pumpkin', 
            13: 'Radish', 
            14: 'Tomato'
        }
        
        result = op[pred]
        return render_template('prediction.html', pred=result)

""" Running our application """
if __name__ == "__main__":
    app.run(debug=True)
