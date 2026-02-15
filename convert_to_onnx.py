"""
Quick ONNX Model Converter
Converts the Keras .h5 model to ONNX format for Vercel deployment
"""
import os
import sys

def main():
    print("=" * 60)
    print("  Converting Keras Model to ONNX")
    print("=" * 60)
    print()
    
    h5_path = 'flask/vegetable_classification.h5'
    onnx_path = 'flask/vegetable_classification.onnx'
    
    # Check if .h5 exists
    if not os.path.exists(h5_path):
        print(f"❌ Error: {h5_path} not found!")
        print("Please train your model first.")
        return False
    
    print(f"📦 Loading model from {h5_path}...")
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported")
    except ImportError as e:
        print(f"❌ TensorFlow not installed: {e}")
        print("Install with: pip install tensorflow")
        return False
    
    try:
        import tf2onnx
        print("✅ tf2onnx imported")
    except ImportError as e:
        print(f"❌ tf2onnx not installed: {e}")
        print("Install with: pip install tf2onnx")
        return False
    
    # Load model
    try:
        model = tf.keras.models.load_model(h5_path, compile=False)
        print(f"✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Convert to ONNX
    print()
    print("🔄 Converting to ONNX format...")
    try:
        # Input spec matching the model's expected input
        spec = (tf.TensorSpec((None, 150, 150, 3), tf.float32, name="input"),)
        
        model_proto, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=spec,
            opset=13,
            output_path=onnx_path
        )
        
        print("✅ Conversion successful!")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Show sizes
    h5_size = os.path.getsize(h5_path) / (1024 * 1024)
    onnx_size = os.path.getsize(onnx_path) / (1024 * 1024)
    
    print()
    print("📊 Results:")
    print(f"   Keras (.h5):  {h5_size:.2f} MB")
    print(f"   ONNX (.onnx): {onnx_size:.2f} MB")
    print()
    print("✅ Done! Model ready for deployment.")
    print()
    print("Next steps:")
    print("  1. git add flask/vegetable_classification.onnx")
    print("  2. git commit -m 'Add ONNX model'")
    print("  3. git push origin main")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
