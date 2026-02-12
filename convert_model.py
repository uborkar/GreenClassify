"""
Convert Keras .h5 model to ONNX format for Vercel deployment
ONNX Runtime is much lighter than TensorFlow (~50MB vs ~500MB)
"""
import os
import sys

# Paths
h5_model_path = 'flask/vegetable_classification.h5'
onnx_model_path = 'flask/vegetable_classification.onnx'

def convert_model():
    """Convert Keras model to ONNX"""
    
    # Check if .h5 model exists
    if not os.path.exists(h5_model_path):
        print(f"❌ Error: Model file not found at {h5_model_path}")
        print("Please train your model first using the Jupyter notebook.")
        return False
    
    print(f"📦 Loading Keras model from {h5_model_path}...")
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(h5_model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    print("\n🔄 Converting to ONNX format...")
    try:
        import tf2onnx
        
        # Convert the model
        spec = (tf.TensorSpec((None, 299, 299, 3), tf.float32, name="input"),)
        output_path = onnx_model_path
        
        model_proto, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=spec,
            opset=13,
            output_path=output_path
        )
        
        print("✅ Conversion successful!")
    except ImportError:
        print("❌ Error: tf2onnx not installed!")
        print("\nPlease install it with:")
        print("   pip install tf2onnx")
        return False
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False
    
    # Show file sizes
    h5_size = os.path.getsize(h5_model_path) / (1024 * 1024)  # MB
    onnx_size = os.path.getsize(onnx_model_path) / (1024 * 1024)  # MB
    
    print("\n📊 Model Size Comparison:")
    print(f"   Keras (.h5):     {h5_size:.2f} MB")
    print(f"   ONNX (.onnx):    {onnx_size:.2f} MB")
    if onnx_size < h5_size:
        print(f"   Size Reduction:  {((h5_size - onnx_size) / h5_size * 100):.1f}%")
    
    print("\n✨ All done! You can now deploy to Vercel.")
    print("\n📝 Next steps:")
    print("   1. git add flask/vegetable_classification.onnx")
    print("   2. git commit -m 'Add ONNX model for deployment'")
    print("   3. git push origin main")
    print("\n💡 Tip: The .h5 file is ignored by git (too large)")
    print("   Only the .onnx file will be deployed to Vercel")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  Keras to ONNX Converter")
    print("  For Vercel Deployment (Lightweight)")
    print("=" * 60)
    print()
    
    success = convert_model()
    
    if not success:
        sys.exit(1)
