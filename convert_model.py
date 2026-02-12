"""
Convert Keras .h5 model to TensorFlow Lite format for Vercel deployment
"""
import os
import tensorflow as tf

# Paths
h5_model_path = 'flask/vegetable_classification.h5'
tflite_model_path = 'flask/vegetable_classification.tflite'

def convert_model():
    """Convert Keras model to TensorFlow Lite"""
    
    # Check if .h5 model exists
    if not os.path.exists(h5_model_path):
        print(f"❌ Error: Model file not found at {h5_model_path}")
        print("Please train your model first using the Jupyter notebook.")
        return False
    
    print(f"📦 Loading Keras model from {h5_model_path}...")
    try:
        model = tf.keras.models.load_model(h5_model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    print("\n🔄 Converting to TensorFlow Lite...")
    try:
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        # Optional: Optimize the model (makes it even smaller)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        
        tflite_model = converter.convert()
        print("✅ Conversion successful!")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False
    
    print(f"\n💾 Saving TFLite model to {tflite_model_path}...")
    try:
        with open(tflite_model_path, 'wb') as f:
            f.write(tflite_model)
        print("✅ TFLite model saved successfully!")
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        return False
    
    # Show file sizes
    h5_size = os.path.getsize(h5_model_path) / (1024 * 1024)  # MB
    tflite_size = os.path.getsize(tflite_model_path) / (1024 * 1024)  # MB
    
    print("\n📊 Model Size Comparison:")
    print(f"   Keras (.h5):        {h5_size:.2f} MB")
    print(f"   TensorFlow Lite:    {tflite_size:.2f} MB")
    print(f"   Size Reduction:     {((h5_size - tflite_size) / h5_size * 100):.1f}%")
    
    print("\n✨ All done! You can now deploy to Vercel.")
    print("   Next steps:")
    print("   1. git add flask/vegetable_classification.tflite")
    print("   2. git commit -m 'Add TFLite model for deployment'")
    print("   3. git push origin main")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  Keras to TensorFlow Lite Converter")
    print("  For Vercel Deployment")
    print("=" * 60)
    print()
    
    convert_model()
