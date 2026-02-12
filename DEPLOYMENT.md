# Converting Model to TensorFlow Lite for Vercel Deployment

## Why TensorFlow Lite?
Vercel has a 250MB limit for serverless functions. Full TensorFlow is too large, so we use TensorFlow Lite which is much smaller.

## How to Convert Your Model

After training your model with the Jupyter notebook, run this Python script to convert it:

```python
import tensorflow as tf

# Load your trained Keras model
model = tf.keras.models.load_model('flask/vegetable_classification.h5')

# Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('flask/vegetable_classification.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted to TensorFlow Lite successfully!")
```

## Quick Conversion Script

You can also use this one-liner in your terminal (after training):

```bash
python -c "import tensorflow as tf; model = tf.keras.models.load_model('flask/vegetable_classification.h5'); converter = tf.lite.TFLiteConverter.from_keras_model(model); tflite_model = converter.convert(); open('flask/vegetable_classification.tflite', 'wb').write(tflite_model); print('Converted!')"
```

## Deployment Checklist

1. ✅ Train your model using the Jupyter notebook
2. ✅ Convert the `.h5` model to `.tflite` format (using script above)
3. ✅ Commit and push both model files to git
4. ✅ Deploy to Vercel

## Local Development vs Production

- **Local Development**: Use `requirements-dev.txt` with full TensorFlow
  ```bash
  pip install -r requirements-dev.txt
  ```

- **Vercel Production**: Uses `requirements.txt` with TensorFlow Lite (automatic)

The Flask app automatically detects which runtime is available and uses the appropriate model format.
