# model_handler.py - REAL MODEL VERSION
import numpy as np
from PIL import Image
import io
import os

class PlantDiseaseModel:
    def __init__(self, model_path='model/plant_model.h5'):
        """Initialize with trained model"""
        self.model_path = model_path
        self.model = None
        self.class_names = []
        self.img_size = (224, 224)
        
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                import tensorflow as tf
                print(f"🧠 Loading trained model from {self.model_path}...")
                self.model = tf.keras.models.load_model(self.model_path)
                print("✅ Real AI model loaded successfully!")
                
                # Load class names
                class_file = 'model/classes.txt'
                if os.path.exists(class_file):
                    with open(class_file, 'r') as f:
                        self.class_names = [line.strip() for line in f.readlines()]
                    print(f"✅ Loaded {len(self.class_names)} disease classes")
                else:
                    print("⚠️ classes.txt not found")
            else:
                print("❌ Trained model not found!")
                print(f"   Expected at: {self.model_path}")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, image):
        """Prepare image for model"""
        if isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        elif isinstance(image, str):
            image = Image.open(image)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = image.resize(self.img_size)
        img_array = np.array(image).astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image):
        """Make prediction using trained model"""
        if self.model is None:
            return {
                'disease_key': 'Model_not_loaded',
                'confidence': 0.0,
                'all_predictions': {},
                'error': 'Model not loaded'
            }
        
        # Preprocess
        processed_img = self.preprocess_image(image)
        
        # Predict
        predictions = self.model.predict(processed_img, verbose=0)
        class_probabilities = predictions[0]
        
        # Get top prediction
        predicted_class_idx = np.argmax(class_probabilities)
        confidence = float(class_probabilities[predicted_class_idx] * 100)
        disease_key = self.class_names[predicted_class_idx]
        
        # All predictions
        all_predictions = {
            self.class_names[i]: float(prob * 100)
            for i, prob in enumerate(class_probabilities)
        }
        
        print(f"🔍 AI Prediction: {disease_key} ({confidence:.1f}%)")
        
        return {
            'disease_key': disease_key,
            'confidence': round(confidence, 2),
            'all_predictions': all_predictions
        }
    
    def get_top_predictions(self, image, top_k=3):
        """Get top K predictions"""
        result = self.predict(image)
        if 'error' in result:
            return []
        
        all_preds = result['all_predictions']
        sorted_preds = sorted(all_preds.items(), key=lambda x: x[1], reverse=True)
        return sorted_preds[:top_k]

if __name__ == '__main__':
    print("Testing Real Model...")
    model = PlantDiseaseModel()
    
    if model.model is not None:
        test_image = Image.new('RGB', (224, 224), color='green')
        result = model.predict(test_image)
        print(f"✓ Works! Prediction: {result['disease_key']}")