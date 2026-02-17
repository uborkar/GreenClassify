import numpy as np
import os
from flask import Flask, request, render_template
from PIL import Image

app = Flask(__name__)

# Model variables
model = None
tflite_interpreter = None

# Model paths
model_path = os.path.join(os.path.dirname(__file__), "vegetable_classification.h5")
tflite_model_path = os.path.join(os.path.dirname(__file__), "vegetable_classification.tflite")

# Try to load TFLite model (for Vercel/production - Python 3.12 compatible)
try:
    import tensorflow as tf
    if os.path.exists(tflite_model_path):
        tflite_interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
        tflite_interpreter.allocate_tensors()
        print("✅ TensorFlow Lite model loaded successfully!")
        print(f"   Model path: {tflite_model_path}")
    else:
        print(f"⚠️ TFLite model not found at {tflite_model_path}")
except ImportError as e:
    print(f"⚠️ TensorFlow not available: {e}")

# Fall back to Keras if TFLite not available (for local development only)
if tflite_interpreter is None:
    try:
        from tensorflow.keras.models import load_model
        if os.path.exists(model_path):
            model = load_model(model_path, compile=False)
            print("✅ Keras model loaded successfully!")
        else:
            print(f"⚠️ Keras model not found at {model_path}")
            print("Please train the model using the Jupyter notebook first.")
    except ImportError:
        print("⚠️ Keras not available")

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    img = Image.open(img_path).convert('RGB')
    img = img.resize((150, 150))  # Model was trained on 150x150
    img_arr = np.array(img, dtype=np.float32)
    # Normalize to [0, 1] range as done during training
    img_arr = img_arr / 255.0
    img_arr = np.expand_dims(img_arr, axis=0)
    return img_arr

def predict_with_model(img_input):
    """Make prediction using available model (TFLite or Keras)"""
    if tflite_interpreter is not None:
        # Use TensorFlow Lite
        input_details = tflite_interpreter.get_input_details()
        output_details = tflite_interpreter.get_output_details()
        tflite_interpreter.set_tensor(input_details[0]['index'], img_input)
        tflite_interpreter.invoke()
        output_data = tflite_interpreter.get_tensor(output_details[0]['index'])
        return np.argmax(output_data)
    elif model is not None:
        # Use Keras
        return np.argmax(model.predict(img_input, verbose=0))
    else:
        return None

# Class mapping
CLASS_NAMES = {
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

# Routes
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
        # Check if model is loaded
        if model is None and tflite_interpreter is None:
            return render_template('prediction.html', 
                pred="⚠️ Model not loaded! Please upload a trained model.")
        
        # Check if file was uploaded
        if 'image' not in request.files:
            return render_template('prediction.html', 
                pred="⚠️ No image file uploaded!")
        
        f = request.files['image']
        
        if f.filename == '':
            return render_template('prediction.html', 
                pred="⚠️ No image selected!")
        
        try:
            # Save uploaded file
            basepath = os.path.dirname(__file__)
            upload_dir = os.path.join(basepath, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            filepath = os.path.join(upload_dir, f.filename)
            f.save(filepath)
            
            # Preprocess and predict
            img_input = preprocess_image(filepath)
            pred = predict_with_model(img_input)
            
            if pred is None:
                return render_template('prediction.html', 
                    pred="❌ Error: Unable to make prediction")
            
            # Get result
            result = CLASS_NAMES.get(pred, "Unknown")
            
            # Clean up uploaded file (optional)
            try:
                os.remove(filepath)
            except:
                pass
            
            return render_template('prediction.html', pred=result)
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template('prediction.html', 
                pred=f"❌ Error: {str(e)}")
    
    return render_template('prediction.html')

@app.route('/health')
def health():
    """Health check endpoint for Vercel"""
    status = {
        'status': 'healthy',
        'model_loaded': model is not None or tflite_interpreter is not None,
        'model_type': 'TFLite' if tflite_interpreter else ('Keras' if model else 'None')
    }
    return status

if __name__ == "__main__":
    app.run(debug=True)
