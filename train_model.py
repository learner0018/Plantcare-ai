# train_model.py
# This script trains a CNN to detect plant diseases
# You're about to train a REAL AI model! 🧠

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

print("="*70)
print("🌱 PLANT DISEASE DETECTION - MODEL TRAINING")
print("="*70)
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
print("="*70)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths
DATASET_DIR = 'dataset/color'  # Where your images are
MODEL_SAVE_PATH = 'model/plant_model.h5'  # Where to save trained model
CLASSES_FILE = 'model/classes.txt'  # List of disease classes

# Training parameters
IMG_SIZE = (224, 224)  # Input image size (width, height)
BATCH_SIZE = 32  # Number of images processed together
EPOCHS = 5  # How many times to go through entire dataset
LEARNING_RATE = 0.001  # How fast the model learns
VALIDATION_SPLIT = 0.2  # 20% of data used for validation

# Create model directory
os.makedirs('model', exist_ok=True)

# ============================================================================
# DATA PREPARATION
# ============================================================================

print("\n📊 STEP 1: Loading and Preparing Data")
print("-"*70)

# Data Augmentation - Creates variations of images to improve learning
# This helps the model generalize better and avoid overfitting
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values to 0-1
    validation_split=VALIDATION_SPLIT,  # Split data for validation
    rotation_range=20,  # Randomly rotate images up to 20 degrees
    width_shift_range=0.2,  # Randomly shift width
    height_shift_range=0.2,  # Randomly shift height
    shear_range=0.2,  # Shear transformation
    zoom_range=0.2,  # Random zoom
    horizontal_flip=True,  # Random horizontal flip
    fill_mode='nearest'  # Fill in missing pixels
)

# Validation data - only rescale, no augmentation
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=VALIDATION_SPLIT
)

# Load training data
print("Loading training images...")
train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',  # One-hot encoded labels
    subset='training',
    shuffle=True
)

# Load validation data
print("Loading validation images...")
validation_generator = val_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Get class information
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print(f"\n✓ Found {train_generator.samples} training images")
print(f"✓ Found {validation_generator.samples} validation images")
print(f"✓ Number of classes: {num_classes}")
print(f"\n📋 Classes detected:")
for i, class_name in enumerate(class_names, 1):
    print(f"  {i}. {class_name}")

# Save class names for later use
with open(CLASSES_FILE, 'w') as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")
print(f"\n✓ Saved class names to: {CLASSES_FILE}")

# ============================================================================
# MODEL ARCHITECTURE
# ============================================================================

print("\n🏗️ STEP 2: Building Neural Network Architecture")
print("-"*70)

# We'll use Transfer Learning with MobileNetV2
# This is a pre-trained model that already knows how to detect features
# We'll adapt it for our specific plant disease task

# Load pre-trained MobileNetV2 (trained on ImageNet)
print("Loading pre-trained MobileNetV2 base model...")
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,  # Remove the classification layer
    weights='imagenet'  # Use weights trained on ImageNet
)

# Freeze the base model - we won't train these layers
# They already know how to detect general features (edges, shapes, etc.)
base_model.trainable = False

print("✓ Base model loaded (MobileNetV2)")
print(f"✓ Base model parameters: {base_model.count_params():,}")

# Build our custom model on top
print("\nBuilding custom classification layers...")
model = keras.Sequential([
    # Input layer
    layers.Input(shape=(224, 224, 3)),
    
    # Pre-trained base model
    base_model,
    
    # Global pooling - converts feature maps to single vector
    layers.GlobalAveragePooling2D(),
    
    # Dropout - prevents overfitting by randomly dropping connections
    layers.Dropout(0.5),
    
    # Dense layer - learns complex patterns
    layers.Dense(128, activation='relu'),
    
    # Another dropout
    layers.Dropout(0.3),
    
    # Output layer - one neuron per disease class
    layers.Dense(num_classes, activation='softmax')
])

print("✓ Model architecture complete!")

# Display model summary
print("\n📐 Model Summary:")
model.summary()

# ============================================================================
# COMPILE MODEL
# ============================================================================

print("\n⚙️ STEP 3: Compiling Model")
print("-"*70)

# Compile model - set up learning process
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',  # Loss function for multi-class
    metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
)

print("✓ Model compiled with:")
print(f"  - Optimizer: Adam (lr={LEARNING_RATE})")
print(f"  - Loss: Categorical Crossentropy")
print(f"  - Metrics: Accuracy, Top-3 Accuracy")

# ============================================================================
# CALLBACKS
# ============================================================================

print("\n📞 Setting up training callbacks...")

# Callback 1: Save best model
checkpoint_callback = keras.callbacks.ModelCheckpoint(
    MODEL_SAVE_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

# Callback 2: Reduce learning rate when stuck
reduce_lr_callback = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=2,
    min_lr=1e-7,
    verbose=1
)

# Callback 3: Stop early if not improving
early_stop_callback = keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

print("✓ Callbacks configured")

# ============================================================================
# TRAIN MODEL
# ============================================================================

print("\n" + "="*70)
print("🚀 STEP 4: TRAINING MODEL")
print("="*70)
print(f"\nTraining will run for up to {EPOCHS} epochs")
print("Each epoch processes the entire dataset once")
print("\n⏰ This may take 30-60 minutes depending on your hardware...")
print("💡 Grab a coffee! ☕\n")

start_time = datetime.now()

# Train the model
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[checkpoint_callback, reduce_lr_callback, early_stop_callback],
    verbose=1
)

end_time = datetime.now()
training_duration = end_time - start_time

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)
print(f"⏱️ Training time: {training_duration}")
print(f"💾 Model saved to: {MODEL_SAVE_PATH}")

# ============================================================================
# EVALUATE MODEL
# ============================================================================

print("\n📊 STEP 5: Evaluating Model Performance")
print("-"*70)

# Evaluate on validation set
val_loss, val_accuracy, val_top3 = model.evaluate(validation_generator, verbose=0)

print(f"\n🎯 Final Validation Metrics:")
print(f"  - Accuracy: {val_accuracy*100:.2f}%")
print(f"  - Top-3 Accuracy: {val_top3*100:.2f}%")
print(f"  - Loss: {val_loss:.4f}")

# ============================================================================
# PLOT TRAINING HISTORY
# ============================================================================

print("\n📈 Generating training visualizations...")

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot accuracy
ax1.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
ax1.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
ax1.set_title('Model Accuracy Over Time', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot loss
ax2.plot(history.history['loss'], label='Training Loss', linewidth=2)
ax2.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
ax2.set_title('Model Loss Over Time', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model/training_history.png', dpi=150, bbox_inches='tight')
print("✓ Saved training plot to: model/training_history.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("🎉 MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*70)
print(f"\n📁 Output files:")
print(f"  - Trained model: {MODEL_SAVE_PATH}")
print(f"  - Class labels: {CLASSES_FILE}")
print(f"  - Training plot: model/training_history.png")
print(f"\n📊 Final Performance:")
print(f"  - Validation Accuracy: {val_accuracy*100:.2f}%")
print(f"  - Training Duration: {training_duration}")
print(f"\n💡 Next steps:")
print(f"  1. Run 'python app.py' to start the web app")
print(f"  2. The app will now use your trained model!")
print(f"  3. Upload plant images to test real disease detection")
print("\n" + "="*70)


## **Step 4: Prepare Your Dataset Structure**

